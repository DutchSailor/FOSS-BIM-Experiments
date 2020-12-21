#Can be used in CPython3 and IronPython

#This pythonfile aims to contain buildingdata and algoritmns not directly linked to a certain software package. They can be used in Revit, FreeCAD, Jupyther etc.

PyBuildingData
PyBData.

		
PyBData.Materials
BaseMaterial
Color

StructuralProperties

FinishMaterial

	DrawingStandards
	Patterns
	Standard
		NL_NEN5104
		NL_Robertsen1990
		NL_3BM
		NL_OpenTopo
		NL_RevitGG
		NL_NEN2580
	
PyBData.Architectural
PyBData.Structural
	StructuralAnalysis
	StructuralSection
		Area
		MomentOfInertia
	
PyBData.MEP
PyBData.BuildingStandardsCodes
	StructuralAnalysis
		TGB1990
		Eurocodes
			EN1990
			EN1991
			NationalAnnex
	Coding #data of all sort of building codes
		Classificationsystem code
			-Source
			-StartYear
			-EndYear
			-Country
		NL
			NL-SFB
			STABU
			Revit SFB-1
			Revit SFB-2
			Revit-SFB-3
			Revit-SFB-4
		International
		Omniclass
	
	
PyBData.AlgoritmnsObjects
	FramingAlgoritmns
		SimpleFace
	PanelAlgoritmns
	
	FramingSystem
	

PyBData.Common
	Framing
	Section #Describe Parametric Profiles
--
	SectionDatabase #Database of steelsections, concretesections and wood dimensions
		
		
		
		
	FramingConnection
		Type
			Beam-Column
			Beam-Beam
			Beam-Beam-Beam
			Beam-Beam-Beam-Beam
			Column-Beam-Beam
			
		Materials
			Generic
			Steel-Steel
			Steel-Wood
				
			Wood-Wood
				
			Steel-Concrete
			Steel
		Parts
			Void
			Plate
			ConnectorSet
				Connector
					Solid
					Void
				
			
			
Parts:

//the framing gows to the hard. T

FramingConnectionType
ConnectingMembers

SteelConnection


PyBData.Helpers
	Primitives
		PointXY
		
		PointXYZ
			def PyBData.Point(x,y,z)
		Line
		Arc
		PolyCurve
	
	Geometry
		Solids
			Extrusion
			SweptBlend
		Conversion
			FreeCAD
			Revit
			Blender
			Sketchup
		PAT
			Create PatternFile
		SVG
			DrawSection
			Draw
	PythonFunctions
		XML
			WriteXML
