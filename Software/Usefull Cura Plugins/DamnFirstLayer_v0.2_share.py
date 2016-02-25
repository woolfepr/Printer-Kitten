#coding: utf8
#Name: Damn First Layer 0.2
#Info: Offers some options for the first layer
#Depend: GCode
#Type: postprocess
#Param: hopOnlyAtDist(float:12.0) Hop at a distance greater or equal ...(mm)
#Param: zLift(float:1.0) Lift Z amount (mm)
#Param: liftSpeed(int:200) Lift speed (mm/s)
#Param: boolInner(bool:True) Use at inner walls?
#Param: boolOuter(bool:True) Use at outer walls?
#Param: boolSkin(bool:True) Use at Skin?
#Param: retractSpeed(int:18000) Speed of retraction
#Param: retractLen(float:5.0) Length of retraction (mm)
#Param: dummy(none:) ---
#Param: dummy(none:) b_WARNING! Be careful at the following options
#Param: dummy(none:) m_Don't set the wall lower than the printbed!\n
#Param: wallNozzleDwn(float:0.1) Go lower for walls, measured at normal height (mm, 0 = normal)
#Param: skinNozzleUp(float:0.1) Go higher for skin - lowers pressure (mm, 0 = normal)
#Param: boolAlt(bool:False) ... alternate (every second line)


# copyright: Florian Dollinger (ataraxis)
# TODO: 1) What comes first? Hopping or retraction?
#       2) retraction speed ok? -> mm/s!
#       3) Speed (by M220 S123.000000)
#       4) alternate
#       5) Objorienterung! z.B. Nozzle


import re


# Vereinfacht das auslesen einer Zeile
def getValue(line, key, default = None):
	if not key in line or (';' in line and line.find(key) > line.find(';')):
		return default
	subPart = line[line.find(key) + 1:]
	m = re.search('^[0-9]+\.?[0-9]*', subPart)
	if m is None:
		return default
	try:
		return float(m.group(0))
	except:
		return default




# Original GCODE einlesen
with open(filename, "r") as f:
	lines = f.readlines()


# Variablen
currSect = ''	# Aktuelle SECTION
layer = ''	# Der aktuelle LAYER
doNth = 0	# Wenn 1, dann wird im weiteren Code nichts mehr verändert.

inTheAir = 0 # Gibt an ob wir den Sprung noch rückgängig machen müssen oder nicht
retracted = False # Gibt an ob das Filament schon retracted wurde
setNozzleForWall = False # Gibt an ob der Nozzle-Abstand für die Wände angepasst wurde
setNozzleForSkin = False # Gibt an ob der Nozzle-Abstand für Skin angepasst wurde

rememberE = 0

lastG1G0 = ''

oldX = 0
oldY = 0
newX = 0
newY = 0

dist = 0

liftSpeed = int(liftSpeed)*60

tmp = 0
actZ = 0
actE = 0.0


	
# Neuen GCODE schreiben
with open(filename, "w") as f:

	# Jede Zeile abarbeiten die zuvor eingelesen wurde
	for line in lines:
		

		# Handelt es sich bei der aktuellen Zeile um einen Kommentar?
		# Wenn, ist es eine neue SECTION oder ein neuer LAYER?
		if line.startswith(';'):
		
			if line.startswith(';TYPE:'):
				currSect = line[6:].strip()
				
			elif line.startswith(';LAYER:'):
				layer = line[7:].strip()
				
			# Schreibe die Zeile unverändert in den neuen GCODE und verhindere weitere Verarbeitung
			f.write(line)
			continue
			
		# Scanne auf G1 und G0 auf einen Z/E-Wert und speichere ihn ggf.
		# dieser wird für den Sprung gebraucht
		
		if getValue(line, 'G', None) == 1 or getValue(line, 'G', None) == 0:
		
			# Alten Z-Wert auslesen, falls gegeben
			tmp = getValue(line, 'Z', None)
			if tmp:
				actZ = tmp
				
			# Alten Z-Wert auslesen, falls gegeben
			tmp = getValue(line, 'E', None)
			if tmp:
				actE = tmp
				
		
		# Setze den Abstand zum Druckbett nach Nutzerangabe für die Wände bzw Skin
		if layer == '0' and (currSect == 'WALL-INNER' or currSect == 'WALL-OUTER') and (setNozzleForWall == False):
		
			# Kleine Sicherheitsabfrage
			if (actZ >= float(wallNozzleDwn)):
				f.write('G0 Z%0.3f; added by DamnFirstLayer\n' % ( actZ - float(wallNozzleDwn) ))
				setNozzleForWall = True
		
		if (layer == '0') and (currSect == 'SKIN') and (setNozzleForSkin == False):
		
				f.write('G0 Z%0.3f; added by DamnFirstLayer\n' % ((float(actZ)) + float(skinNozzleUp)))
				setNozzleForWall = False
				setNozzleForSkin = True
			

			
		# Falls es sich um einen G0-Code handelt und wir im ersten Layer sind...
		if getValue(line, 'G', None) == 0 and layer == '0':
		
			# Berechne den Abstand der 'übersprungen' wird, falls dies nicht die erste Bewegung ist
			if lastG1G0 <> '':
				oldX = getValue(lastG1G0, 'X', oldX)
				oldY = getValue(lastG1G0, 'Y', oldY)
				
				newX = getValue(line, 'X', newX)
				newY = getValue(line, 'Y', newY)
				
				dist = ( (oldX-newX)**2 + (oldY-newY)**2 )**.5
				
			
			# ... und um den Bereich WALL-INNER, WALL-OUTER oder SKIN handelt

			if (currSect == 'WALL-INNER' and bool(boolInner) == True) or \
			   (currSect == 'WALL-OUTER' and bool(boolOuter) == True) or \
			   (currSect == 'SKIN' and bool(boolSkin) == True):
			
				# Wir springen nur, wenn wir nicht bereits in der Luft sind
				# und die minimale Sprungdistanz erreicht ist
				
				if inTheAir == 0 and dist >= hopOnlyAtDist:
					inTheAir = 1
					
					
					# Evtl doch nach Sprung Filament zurückholen?
					if retracted == False:
						f.write('G1 E%1.5f F%i ;added by DamnFirstLayer\n' % ((float(actE) - float(retractLen)), int(retractSpeed)))
						rememberE = actE
						retracted = True
					
					
					# Der Sprung
					if setNozzleForWall == True:
						f.write("G0 Z%.3f F%i; added by DamnFirstLayer\n" % (actZ + zLift - wallNozzleDwn, liftSpeed) )
					elif setNozzleForSkin == True:
						f.write("G0 Z%.3f F%i; added by DamnFirstLayer\n" % (actZ + zLift + skinNozzleUp, liftSpeed) )
					else:
						f.write("G0 Z%.3f F%i; added by DamnFirstLayer\n" % (actZ + zLift, liftSpeed ))

					
					# Travel-Befehl
					f.write(line)
					

				else:
					f.write(line)

				
			else:
				f.write(line)
				
				
		
		# Beim nächsten G1 zurückspringen
		elif getValue(line, 'G', None) == 1 and layer == '0' and inTheAir == 1:
			inTheAir = 0
			
			#Sprung zurück
			if setNozzleForWall == True:
				f.write("G0 Z%f F%s; added by DamnFirstLayer\n"%(actZ-wallNozzleDwn, liftSpeed))
			elif setNozzleForSkin == True:
				f.write("G0 Z%f F%s; added by DamnFirstLayer\n"%(actZ+skinNozzleUp, liftSpeed))
			else:
				f.write("G0 Z%f F%s; added by DamnFirstLayer\n"%(actZ, liftSpeed))
			
			if retracted == True:
				f.write('G1 E%1.5f F%i ;added by DamnFirstLayer\n' % ((float(rememberE)), float(retractSpeed)))
				retracted = False
				
			f.write(line)
			
		else:
			if retracted == True:
				f.write('G1 E%1.5f F%i ;added by DamnFirstLayer\n' % ((float(rememberE)), float(retractSpeed)))
				retracted = False
				
			f.write(line)
		
		
		
		
		
		# Speichere die letzte G1/G0-Codezeile zur Abstandsberechnung
		if getValue(line, 'G', None) == 1 or getValue(line, 'G', None) == 0:
			lastG1G0 = line