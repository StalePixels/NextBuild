#include <nextlib.bas>
NextReg($7,2)								' 14mhz lets not muck around 
' NextReg($43,$1)						' ULANext control reg
' NextReg($42,15)						' ULANext number of inks : 255 127 63 41 15 7 
' NextReg($14,$0)  					' black global transparency value 
' NextReg($40,$b)    				' $40 Palette Index Register  I assume that colours 0-7 ink 8-15 bright ink 16+ paper in ULA mode
' NextReg($41,$0)  					' value of index position 

paper 0: ink 7 : border 0 : cls 	

LoadSD("aliens.spr",49152,16384,0)
InitSprites(16,49152) 
NextReg($15,%00001001)  	' Enable sprite visibility & Sprite ULA L2 order 

dim inpos as ubyte
dim outpos,px,py,ship as ubyte
dim cmd,outcmd,keytimer,keytimer2,procb,fdown as ubyte

ShowLayer2(1)
ship=7 : py = 192 : keytimer2=0

for x = 0 to 7
	cmd=x
	Fifo(@ddata,0)
next 

dim timer as ubyte=10
do 

	WaitFrame()
	timer=timer-1
	'if timer=0
		Fifo(@ddata,1) ' read fifo 
		'print cmd 
	'	print at 0,0;ink 7; "     " 
	'	timer=50
	'endif 

	if cmd = 1
		
		poke(@bullets+cast(uinteger,outcmd*3),1)		
		poke(@bullets+cast(uinteger,outcmd*3)+1,px)		
		poke(@bullets+cast(uinteger,outcmd*3)+2,192)		
		pfire=5 : ship = 8 
	endif 

	'procb=1-procb
	procb=1
	if procb
		for x=0 to 7
			if peek(@bullets+cast(uinteger,x*3))=1
				 bx=peek(@bullets+cast(uinteger,x*3)+1)
				 by=peek(@bullets+cast(uinteger,x*3)+2)
				 if by>0
					by = by -4 
					poke(@bullets+cast(uinteger,x*3)+2,by)
				 else 
					poke(@bullets+cast(uinteger,x*3),0)
					
				 endif
			endif
			UpdateSprite(32+bx,by+6,x+10,12,0,0)
			UpdateSprite(32+px,py,1,ship,0,0)
		next 
		if pfire>0
			if ship<11 : ship=ship+1 : else ship = 7 : endif
			if py>192 : py=py-1: endif 
			pfire=pfire-1
		endif 
	endif 
	

	
	f = in $7ffe band 3
	if f=2 and keytimer=0 and fdown=0
		beep .1,3
		cmd=1
		Fifo(@ddata,0)
		keytimer=5
		py=py+2
		fdown=1
	elseif f>2
		fdown=0
	endif 
	k = in $dffe band %00000011 
	if k =1 'and 'keytimer2=0
		dir=1 : d = 6 
	elseif k = 2 'and keytimer2=0
		dir=2 : d = 6 
	endif 
	
	if dir=1			' left 
		if px+d>16 then px=px-1-(d)
		d=d-1
		if d=0 : dir = 0 : d = 0 : endif 
	elseif dir=2
		if px+d<255-32  then px=px+1+(d)
		d=d-1
		if d=0 : dir = 0 : d = 0 : endif 
	endif 
	
	if keytimer>0 : keytimer=keytimer-1 : endif 
	'if keytimer2>0 : keytimer2=keytimer2-1 : endif 

loop 

 
Sub WaitFrame()

	ASM 
		wait:   
			ld hl,pretim        
			ld a,(23672)        ; current timer  
			sub (hl)             
			cp 1                ; two frames elapsed yet?
			jr nc,wait0         ; yes, no more delay 
			jp wait
			ld bc,0
			ret
		wait0:  
			ld a,(23672)        ; current timer
			ld (hl),a          ; store this setting
			ld bc,1
			jp fraout
		pretim:
		defb 0
		fraout:		
	END ASM

end sub

asm 
	BREAK 
END ASM 

pause 0 

sub Fifo(byval address as uinteger, byval mode as ubyte)

	if mode = 0 ' write to fifo 
		' write to fifo 
		v=peek(@ddata+cast(uinteger,inpos))
		if v = 0 	' fifo empty
			' store cmd 
			poke @ddata+cast(uinteger,inpos),cmd
			'print at 0,inpos*2;ink 7; cmd
			else 
			cmd = 255 
		endif 
		if inpos<7 : inpos=inpos+1 : ELSE : inpos=0 : ENDIF  
		
	else 
		' read fifo 
		cmd=peek(@ddata+cast(uinteger,outpos))	
		'print at 0,outpos*2;ink 7; "0"
		outcmd=outpos
		poke @ddata+cast(uinteger,outpos),0		' remove object 
		if outpos<7 : outpos=outpos+1 : ELSE : outpos=0 : ENDIF 
		
	endif 
	
end sub 


ddata:
ASM 
	ddata:
	; 8 spaces in our FIFO 
	DB 0,0,0,0,0,0,0,0	
END ASM 

bullets:
asm 
	; actve, x,y bullets 
	DB 0,0,0, 0,0,0, 0,0,0, 0,0,0
	DB 0,0,0, 0,0,0, 0,0,0, 0,0,0
end asm 
           