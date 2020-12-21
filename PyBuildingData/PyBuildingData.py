# Helpers

    #Primitives
		def PointXY(x,y)

		def PointXYZ(x,y,z)

        def Line2D(PointXY,PointXY)

		def Arc2D(PointXY,PointXY,PointXY)

		def PolyCurve

        sqrt2 = 1.414213562 # Squareroot of number 2

    def find_in_list_of_list(mylist, char):
        for sub_list in mylist:
            if char in sub_list:
                return (mylist.index(sub_list))
        raise ValueError("'{char}' is not in list".format(char=char))


# Py Building Data

def PyBData.Common
     #PyBData.Common.Framing
	
	#PyBData.Common.Section
	#Describe Parametric Profiles
	#def Section
		
	#Aluminium

        #Steel
            def parameters


            def C-channel_parallel_flange(Section)
                Description = "C-channel with parallel flange"
                ID = "C_PF"

                #parameters
                b = Section.b #width
                h = Sectopm.h #height
                tf = Section.tf #flange thickness
                tw = Section.tw #web thickness
                r = Section.r #web fillet
                e = Section.e #centroid horizontal

                #describe points
                p1 = [-e,-h/2] #left bottom
                p2 = [b-e,-h/2] #right bottom
                p3 = [b-e,-h/2+tf] 
                p4 = [-e+tw+r,-h/2+tf] #start arc
                p5 = [-e+tw+r-r1,-h/2+tf+r-r1] #second point arc
                p6 = [-e+tw,-h/2+tf+r] #end arc
                p7 = [-e+tw,h/2-tf-r] #start arc
                p8 = [-e+tw+r-r1,h/2-tf-r+r1] #second point arc
                p9 = [-e+tw+r,h/2-tf] #end arc
                p10 = [b-e,h/2-tf]
                p11 = [b-e,h/2] #right top
                p12 = [-e,h/2] #left top

                #describe curves
                l1 = line2D(p1,p2)
                l2 = line2D(p2,p3)
                l3 = line2D(p3,p4)
                l3 = arc2D(p4,p5,p6)
                l4 = line2D(p6,p7)
                l5 = arc2D(p7,p8,p9)
                l6 = line2D(p9,p10)
                l7 = line2D(p10,p11)
                l8 = line2D(p11,p12)
                l9 = line2D(p12,p1)

                curve = [l1,l2,l3,l4,l5,l6,l7,l8,l9]

            def C-channel_sloped_flange(Section)
                Description = "C-channel with sloped flange"
                ID = "C_SF"

                #parameters
                b = Section.b #width
                h = Sectopm.h #height
                tf = Section.tf #flange thickness
                tw = Section.tw #web thickness
                r1 = Section.r1 #web fillet
                r11 = r1/sqrt2
                r2 = Section.r2 #flange fillet
                r21 = r2/sqrt2
                tl = Section.tl #flange thickness location from right
                sa = Section.sa #the angle of sloped flange in degrees
                e = Section.e #centroid horizontal

                #describe points
                #describe points
                p1 = [-e,-h/2] #left bottom
                p2 = [b-e,-h/2] #right bottom
                p3 = [b-e,-h/2+tf-math.tan(sa)*tl-r2] #start arc
                p4 = [b-e-r2+r21,-h/2+tf-math.tan(sa)*tl-r2+r21] #second point arc
                p5 = [b-e-r2+math.sin(sa)*r2,-h/2+tf-math.tan(sa)*(tl-r2)] #end arc
                p6 = [-e+tw+r1-math.sin(sa)*r1,-h/2+tf+math.tan(sa)*(b-tl-tw-r1)] #start arc
                p7 = [-e+tw+r1-r11,-h/2+tf+math.tan(sa)*(b-tl-tw-r1)+r1-r11] #second point arc
                p8 = [-e+tw,-h/2+tf+math.tan(sa)*(b-tl-tw)+r1] #end arc
                p9 = [p8[0],-p8[1]] #start arc
                p10 = [p7[0],-p7[1]] #second point arc
                p11 = [p6[0],-p6[1]] #end arc
                p12 = [p5[0],-p5[1]] #start arc
                p13 = [p4[0],-p4[1]] #second point arc
                p14 = [p3[0],-p3[1]] #end arc
                p15 = [p2[0],-p2[1]] #right top
                p16 = [p1[0],-p1[1]] #left top
                
                #describe curves
                l1 = line2D(p1,p2)
                l2 = line2D(p2,p3)
                l3 = arc2D(p3,p4,p5)
                l4 = line2D(p5,p6)
                l5 = arc2D(p6,p7,p8)
                l6 = line2D(p8,p9)
                l7 = arc2D(p9,p10,p11)
                l8 = line2D(p11,p12)
                l9 = arc2D(p12,p13,p14)
                l10 = line2D(p14,p15)
                l11 = line2D(p15,p16)
                l12 = line2D(p16,p1)

                curve = [l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12]

            def I-shape_parallel_flange(Section)
                Description = "I Shape profile with parallel flange"
                ID = "I_PF"

                #parameters
                b = Section.b #width
                h = Section.h #height
                tf = Section.tf #flange thickness
                tw = Section.tw #web thickness
                r = Section.r #web fillet
                r1 = r/sqrt2
                
                #describe points 
                p1 = [b/2,-h/2] #right bottom
                p2 = [b/2,-h/2+tf]
                p3 = [tw/2+r,-h/2+tf] #start arc
                p4 = [tw/2+r-r1,(-h/2+tf+r-r1)] #second point arc
                p5 = [tw/2,-h/2+tf+r] #end arc
                p6 = [tw/2,h/2-tf-r] #start arc
                p7 = [tw/2+r-r1,h/2-tf-r+r1] #second point arc
                p8 = [tw/2+r,h/2-tf] #end arc
                p9 = [b/2,h/2-tf]
                p10 = [b/2),(h/2] #right top
				p11 = [-p10[0],p10[1]] #left top
				p12 = [-p9[0],p9[1]]
				p13 = [-p8[0],p8[1]] #start arc
				p14 = [-p7[0],p7[1]] #second point arc
				p15 = [-p6[0],p6[1]] #end arc
				p16 = [-p5[0],p5[1]] #start arc
				p17 = [-p4[0],p4[1]] #second point arc
				p18 = [-p3[0],p3[1]] #end arc
				p19 = [-p2[0],p2[1]]
				p20 = [-p1[0],p1[1]]

                #describe curves
                l1 = line2D(p1,p2)
                l2 = line2D(p2,p3)
                l3 = arc2D(p3,p4,p5)
                l4 = line2D(p5,p6)
                l5 = arc2D(p6,p7,p8)
                l6 = line2D(p8,p9)
                l7 = line2D(p9,p10)
                l8 = line2D(p10,p11)
                l9 = line2D(p11,p12)
                l10 = line2D(p12,p13)
                l11 = arc2D(p13,p14,p15)
                l12 = line2D(p15,p16)
                l13 = arc2D(p16,p17,p18)
                l14 = line2D(p18,p19)
                l15 = line2D(p19,p20)
                l16 = line2D(p20,p1)

                curve = [l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16]

		        ("steelprofilename", "h", "bf", "tf", "tw", "r", "I-shape parallel flange"),

            def L_angle(Section)
                Description = "L-angle""
                ID = "L"

                #parameters
                b = Section.b #width
                h = Section.h #height
                tw = Section.tw #wall nominal thickness
                tf = tw
                r1 = Section.r1 #inner fillet
                r11 = r1/math.sqrt(2)
                r2 = Section.r2 #outer fillet
                r21 = r2/math.sqrt(2)
                ex = obj.CentroidHorizontal.Value #from left
                ey = obj.CentroidVertical.Value #from bottom

                #describe points
                p1 = [-ex,-ey] #left bottom
                p2 = [b-ex,-ey] #right bottom
                p3 = [b-ex,-ey+tf-r2] #start arc
                p4 = [b-ex-r2+r21,-ey+tf-r2+r21] #second point arc
                p5 = [b-ex-r2,-ey+tf] #end arc
                p6 = [-ex+tf+r1,-ey+tf] #start arc
                p7 = [-ex+tf+r1-r11,-ey+tf+r1-r11] #second point arc
                p8 = [-ex+tf,-ey+tf+r1] #end arc
                p9 = [-ex+tf,h-ey-r2] #start arc
                p10 = [-ex+tf-r2+r21,h-ey-r2+r21] #second point arc
                p11 = [-ex+tf-r2,h-ey] #end arc
                p12 = [-ex,h-ey] #left top

                #describe curves
                l1 = line2D(p1,p2)
                l2 = line2D(p2,p3)
                l3 = arc2D(p3,p4,p5)
                l4 = line2D(p5,p6)
                l5 = arc2D(p6,p7,p8)
                l6 = line2D(p8,p9)
                l7 = arc2D(p9,p10,p11)
                l8 = line2D(p11,p12)
                l9 = line2D(p12,p1)

                curve = [l1,l2,l3,l4,l5,l6,l7,l8,l9]

            def rectangle_hollow_section(Section)
                Description = "rectangle hollow section"
                ID = "RHS"

                #parameters
                b = Section.b #width
                h = Section.h #height
                t = Section.t #wall nominal thickness
                r1 = Section.r1 #inner fillet
                r2 = Section.r2 #outer fillet

                #describe points

                #outer curve
                p1 = [b/2-r1,-h/2] #right bottom start arc
                p2 = [b/2-r1+r11,-h/2+r1-r11] #right bottom second point arc
                p3 = [b/2,-h/2+r1] #right bottom end arc
                p4 = [p3[0],-p3[1]] #right top start arc
                p5 = [p2[0],-p2[1]] #right top second point arc
                p6 = [p1[0],-p1[1]] #right top end arc
                p7 = [-p6[0],p6[1]] #left top start arc
                p8 = [-p5[0],p5[1]] #left top second point arc
                p9 = [-p4[0],p4[1]] #left top end arc
                p10 = [p9[0],-p9[1]] #left bottom start arc
                p11 = [p8[0],-p8[1]] #left bottom second point arc
                p12 = [p7[0],-p7[1]] #left bottom end arc
                
                #inner curve

                q1 = [b/2-t-r2,-h/2+t] #right bottom start arc
                q2 = [b/2-t-r2+r21,-h/2+t+r2-r21] #right bottom second point arc
                q3 = [b/2-t,-h/2+t+r2] #right bottom end arc
                q4 = [q3[0],-q3[1]] #right top start arc
                q5 = [q2[0],-q2[1]] #right top second point arc
                q6 = [q1[0],-q1[1]] #right top end arc
                q7 = [-q6[0],q6[1]] #left top start arc
                q8 = [-q5[0],q5[1]] #left top second point arc
                q9 = [-q4[0],q4[1]] #left top end arc
                q10 = [q9[0],-q9[1]] #left bottom start arc
                q11 = [q8[0],-q8[1]] #left bottom second point arc
                q12 = [q7[0],-q7[1]] #left bottom end arc

                #CURVES TO ADD


		#ConcreteCastInPlace
		#ConcretePrecast
		#Wood
	
	SectionDatabase #Database of steelsections, concretesections and wood dimensions
		
		
# Concrete

def concrete_shapes(shapename):
    shape_data = ["rectangle shape",
                  "round shape",
                  "H-shape",
                  "U-shape",
                  "L-shape",
                  "T-shape",
                  "RHS-shape",
                  "CHS-shape",
                  "cross-shape"
                  ]
    return "test"


# Steel
# profile means for coldformed steel
# otherwise a section is hotrolled or welded

def steel_profiles(profilename):
    shape_data = [("C-profile"),
                  ("C-profile with fold"),
                  ("C-profile with lips"),
                  ("C-channel parallel flange"), #done
                  ("C-channel sloped flange"), #done
                  ("I-shape parallel flange"), #done
                  ("I-shape sloped flange"),
                  ("I-shape welded"),
                  ("I-split parallel flange"),
                  ("I-split sloped flange"),
                  ("L-profile"), #done
                  ("L-profile with lips"),
                  ("L-angle"),
                  ("pipe standard"),
                  ("rectangle bar"),
                  ("rectangle hollow section"),
                  ("round"),
                  ("round hollow section",),
                  ("sigma profile"),
                  ("sigma profile with fold"),
                  ("sigma profile with lips"),
                  ("T-shape"),
                  ("Z-profile"),
                  ("Z-profile with lips")
                  ]

    steelprofile_data =[("HEA100",96,100,5,8,12,"I-shape parallel flange"),
                       ("HEA120",114,120,5,8,12,"I-shape parallel flange"),
                       ("HEA140",133,140,6,9,12,"I-shape parallel flange"),
                       ("HEA160",152,160,6,9,15,"I-shape parallel flange"),
                       ("HEA180",171,180,6,10,15,"I-shape parallel flange"),
                       ("HEA200",190,200,7,10,18,"I-shape parallel flange"),
                       ("HEA220",210,220,7,11,18,"I-shape parallel flange"),
                       ("HEA240",230,240,8,12,21,"I-shape parallel flange"),
                       ("HEA260",250,260,8,13,24,"I-shape parallel flange"),
                       ("HEA280",270,280,8,13,24,"I-shape parallel flange"),
                       ("HEA300",290,300,9,14,27,"I-shape parallel flange"),
                       ("HEA320",310,300,9,16,27,"I-shape parallel flange"),
                       ("HEA360",350,300,10,18,27,"I-shape parallel flange"),
                       ("HEA400",390,300,11,19,27,"I-shape parallel flange"),
                       ("HEA450",440,300,12,21,27,"I-shape parallel flange"),
                       ("HEA500",490,300,12,23,27,"I-shape parallel flange"),
                       ("HEA550",540,300,13,24,27,"I-shape parallel flange"),
                       ("HEA600",590,300,13,25,27,"I-shape parallel flange"),
                       ("HEA650",640,300,14,26,27,"I-shape parallel flange"),
                       ("HEA700",690,300,15,27,27,"I-shape parallel flange"),
                       ("HEA800",790,300,15,28,30,"I-shape parallel flange"),
                       ("HEA900",890,300,16,30,30,"I-shape parallel flange"),
                       ("HEA1000",990,300,17,31,30,"I-shape parallel flange"),
                       ("HEB100",100,100,6,10,12,"I-shape parallel flange"),
                       ("HEB120",120,120,7,11,12,"I-shape parallel flange"),
                       ("HEB140",140,140,7,12,12,"I-shape parallel flange"),
                       ("HEB160",160,160,8,13,15,"I-shape parallel flange"),
                       ("HEB180",180,180,9,14,15,"I-shape parallel flange"),
                       ("HEB200",200,200,9,15,18,"I-shape parallel flange"),
                       ("HEB220",220,220,10,16,18,"I-shape parallel flange"),
                       ("HEB240",240,240,10,17,21,"I-shape parallel flange"),
                       ("HEB260",260,260,10,18,24,"I-shape parallel flange"),
                       ("HEB280",280,280,11,18,24,"I-shape parallel flange"),
                       ("HEB300",300,300,11,19,27,"I-shape parallel flange"),
                       ("HEB320",320,300,12,21,27,"I-shape parallel flange"),
                       ("HEB340",340,300,12,22,27,"I-shape parallel flange"),
                       ("HEB360",360,300,13,23,27,"I-shape parallel flange"),
                       ("HEB400",400,300,14,24,27,"I-shape parallel flange"),
                       ("HEB450",450,300,14,26,27,"I-shape parallel flange"),
                       ("HEB500",500,300,15,28,27,"I-shape parallel flange"),
                       ("HEB550",550,300,15,29,27,"I-shape parallel flange"),
                       ("HEB600",600,300,16,30,27,"I-shape parallel flange"),
                       ("HEB650",650,300,16,31,27,"I-shape parallel flange"),
                       ("HEB700",700,300,17,32,27,"I-shape parallel flange"),
                       ("HEB800",800,300,18,33,30,"I-shape parallel flange"),
                       ("HEB900",900,300,19,35,30,"I-shape parallel flange"),
                       ("HEB1000",1000,300,19,36,30,"I-shape parallel flange"),
                       ("HEM100",120,106,12,20,12,"I-shape parallel flange"),
                       ("HEM120",140,126,13,21,12,"I-shape parallel flange"),
                       ("HEM140",160,146,13,22,12,"I-shape parallel flange"),
                       ("HEM160",180,166,14,23,15,"I-shape parallel flange"),
                       ("HEM180",200,186,15,24,15,"I-shape parallel flange"),
                       ("HEM200",220,206,15,25,18,"I-shape parallel flange"),
                       ("HEM220",240,226,16,26,18,"I-shape parallel flange"),
                       ("HEM240",270,248,18,32,21,"I-shape parallel flange"),
                       ("HEM260",290,268,18,33,24,"I-shape parallel flange"),
                       ("HEM280",310,288,19,33,24,"I-shape parallel flange"),
                       ("HEM300",340,310,21,39,27,"I-shape parallel flange"),
                       ("HEM320",359,309,21,40,27,"I-shape parallel flange"),
                       ("HEM340",377,309,21,40,27,"I-shape parallel flange"),
                       ("HEM360",395,308,21,40,27,"I-shape parallel flange"),
                       ("HEM400",432,307,21,40,27,"I-shape parallel flange"),
                       ("HEM450",478,307,21,40,27,"I-shape parallel flange"),
                       ("HEM500",524,306,21,40,27,"I-shape parallel flange"),
                       ("HEM550",572,306,21,40,27,"I-shape parallel flange"),
                       ("HEM600",620,305,21,40,27,"I-shape parallel flange"),
                       ("HEM650",668,305,21,40,27,"I-shape parallel flange"),
                       ("HEM700",716,304,21,40,27,"I-shape parallel flange"),
                       ("HEM800",814,303,21,40,30,"I-shape parallel flange"),
                       ("HEM900",910,302,21,40,30,"I-shape parallel flange"),
                       ("HEM1000",1008,302,21,40,30,"I-shape parallel flange"),
                       ("IPE80",80,3.8,46,5.2,5,"I-shape parallel flange"),
                       ("IPE100",100,4.1,55,5.7,7,"I-shape parallel flange"),
                       ("IPE120",120,4.4,64,6.3,7,"I-shape parallel flange"),
                       ("IPE140",140,4.7,73,6.9,7,"I-shape parallel flange"),
                       ("IPE160",160,5,82,7.4,9,"I-shape parallel flange"),
                       ("IPE180",180,5.3,91,8,9,"I-shape parallel flange"),
                       ("IPE200",200,5.6,100,8.5,12,"I-shape parallel flange"),
                       ("IPE220",220,5.9,110,9.2,12,"I-shape parallel flange"),
                       ("IPE240",240,6.2,120,9.8,15,"I-shape parallel flange"),
                       ("IPE270",270,6.6,135,10.2,15,"I-shape parallel flange"),
                       ("IPE300",300,7.1,150,10.7,15,"I-shape parallel flange"),
                       ("IPE330",330,7.5,160,11.5,18,"I-shape parallel flange"),
                       ("IPE360",360,8,170,12.7,18,"I-shape parallel flange"),
                       ("IPE400",400,8.6,180,13.5,21,"I-shape parallel flange"),
                       ("IPE450",450,9.4,190,14.6,21,"I-shape parallel flange"),
                       ("IPE500",500,10.2,200,16,21,"I-shape parallel flange"),
                       ("IPE550",550,11.1,210,17.2,24,"I-shape parallel flange"),
                       ("IPE600",600,12,220,19,24,"I-shape parallel flange"),
                       ("UNP80",80,45,6,8,"C-channelslopedflange"),
                       ("UNP100",100,50,6,9,"C-channelslopedflange"),
                       ("UNP120",120,55,7,9,"C-channelslopedflange"),
                       ("UNP140",140,60,7,10,"C-channelslopedflange"),
                       ("UNP160",160,65,8,11,"C-channelslopedflange"),
                       ("UNP180",180,70,8,11,"C-channelslopedflange"),
                       ("UNP200",200,75,9,12,"C-channelslopedflange"),
                       ("UNP220",220,80,9,13,"C-channelslopedflange"),
                       ("UNP240",240,85,10,13,"C-channelslopedflange"),
                       ("UNP260",260,90,10,14,"C-channelslopedflange"),
                       ("UNP280",280,95,10,15,"C-channelslopedflange"),
                       ("UNP300",300,100,10,16,"C-channelslopedflange"),
                       ("UNP320",320,100,14,18,"C-channelslopedflange"),
                       ("UNP350",350,100,14,16,"C-channelslopedflange"),
                       ("UNP380",380,102,14,16,"C-channelslopedflange"),
                       ("UNP400",400,110,14,18,"C-channelslopedflange"),
                       ("UPE80",80,50,4.5,8,10,"C-channelparallelflange"),
                       ("UPE100",100,55,5,8.5,10,"C-channelparallelflange"),
                       ("UPE120",120,60,5.5,9,10,"C-channelparallelflange"),
                       ("UPE140",140,65,6,9.5,10,"C-channelparallelflange"),
                       ("UPE160",160,70,6.5,10,12,"C-channelparallelflange"),
                       ("UPE180",180,75,7,10.5,12,"C-channelparallelflange"),
                       ("UPE200",200,80,7.5,11,12,"C-channelparallelflange"),
                       ("UPE220",220,85,8,12,12,"C-channelparallelflange"),
                       ("UPE240",240,90,8.5,13,15,"C-channelparallelflange"),
                       ("UPE270",270,95,9,14,15,"C-channelparallelflange"),
                       ("UPE300",300,100,9.5,15,15,"C-channelparallelflange"),
                       ("UPE330",330,105,11,16,18,"C-channelparallelflange"),
                       ("UPE360",360,110,12,17,18,"C-channelparallelflange"),
                       ("UPE400",400,115,13.5,18,18,"C-channelparallelflange")
                       ]
    steelprofile_sublist = steelprofile_data[find_in_list_of_list(steelprofile_data, profilename)]
    parameternames_sublist = shape_data[find_in_list_of_list(shape_data, steelprofile_sublist[-1])]
    return steelprofile_sublist, parameternames_sublist


name_profile = "HEA200"

profile_data = steel_profiles(name_profile)[0]

profile_name = profile_data[0]
b = profile_data[2]
h = profile_data[1]
tw = profile_data[4]
tf = profile_data[3]
r = profile_data[5]

print(b)
print(h)
print(tw)
print(tf)
print(r)