import sqlite3

def infoExamenes():
	#CODIGO,NOMBRE,PRECIO

	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS INFOEXAMENES (CODIGO INTEGER PRIMARY KEY, DESCRIPCION TEXT, PRECIO NUMERIC, IDGRUPO INT)")

	cursor.execute("SELECT * FROM INFOEXAMENES")
	validate = cursor.fetchall()

	if validate == []:
		data = [
		(1,"% SATURACIÓN(TRANSFERRINA)",5, 2),
		(2,"17 - HIDROXI-PROGESTERONA",15, 8),
		(3,"17 - HRIDOXI-ANDROSTENEIDONA",15, 8),
		(4,"ACIDO B2 GLICOPROTEINA(IGG)",15),
		(5,"ACIDO B2 GLICOPROTEINA(IGM)",15),
		(6,"ACIDO URICO",2, 1),
		(7,"ACIDO URICO EN ORINA 24H",3, 6),
		(8,"ACIDO URICO EN ORINA CASUAL",3, 6),
		(9,"ACIDO ANTI-DNA",12),
		(10,"ACIDO FOLICO",20, 9),
		(11,"ACTH",20, 8),
		(12,"ADENOVIRUS(HECES)",0, 3),
		(13,"ALFA-FETOPROTEINA(AFP)",10),
		(14,"AMILASA SERICA",5, 2),
		(15,"AMONIO",10),
		(16,"AMONIO POST PANDRIAL",10),
		(17,"ANCA",10),
		(18,"ANDROSTENEIDOA",15, 8),
		(19,"ANTI CARCINOEMBRIONARIO(CEA)",10, 10),
		(20,"ANTI CCP(ANTIPEPTIDO CITRUNILADO)",18, 7),
		(21,"ANTI E",10, 7),
		(22,"ANTI JO-1",10),
		(23,"ANTI SCL 70",10),
		(24,"ANTICORE",0),
		(25,"ANTI-CORE(IGG)",0, 7),
		(26,"ANTI-CORE(IGM)",0, 7),
		(27,"ANTICUERPOS ANTI B2 GLICOPROTEINAS(IGG)",15),
		(28,"ANTICUERPOS ANTI B2 GLICOPROTEINAS(IGM)",15),
		(29,"ANTICUERPOS ANTI - RO(SS-A)",15),
		(30,"ANTICUERPOS ANTI - LA(SS-B)",15),
		(31,"ANTICUERPOS ANTICARDIOLIPINAS(IGG)",15),
		(32,"ANTICUERPOS ANTICARDIOLIPINAS(IGM)",15),
		(33,"ANTICUERPOS ANTIFOSFOLIPIDOS",30),
		(34,"ANTICUERPOS ANTINUCLEARES(ANA)",16),
		(35,"ANTICUERPOS ANTITIROIDEOS",16),
		(36,"ANTI-DNA",12, 10),
		(37,"ANTIGENO PROSTATICO(PSA)",8, 10),
		(38,"ANTIGENO PROSTATICO(LIBRE)",8, 10),
		(39,"ANTIGENOS FEBRILES",5, 7),
		(40,"ANTIMICROSOMALES",0, 8),
		(41,"ANTIMITOCONDRIALES",10, 8),
		(42,"ANTIPEROXIDASA(TPO)",10, 8),
		(43,"ANTITIROGLOBULINA",10, 8),
		(44,"APLICADORES DE MADERA S/ALGODON X", 500.0),
		(45,"ASTO(ANTIESTREPTOLISINA O)",3, 7),
		(46,"AZUCARES REDUCTORES",2, 3),
		(47,"BETA 2 MICROGLOBULINA",15),
		(48,"BHCG(HCG CUANTITATIVO)",5, 8),
		(49,"BILIRRUBINA TOTAL Y FRACCIONADA",3, 1),
		(50,"CA - 125",10, 10),
		(51,"CA - 15 - 3",10, 10),
		(52,"CA - 19 - 9",10, 10),
		(53,"CALCIO EN ORINA 24H",2, 6),
		(54,"CALCIO EN ORINA PARCIAL",2, 6),
		(55,"CALCIO SERICO",2, 1),
		(56,"CARBAMANZEPINA",0, 9),
		(57,"CARGA GLYCOLAB",3, 1),
		(58,"CELULAS L.E.",0),
		(59,"CH - 50",10, 10),
		(60,"CHAGAS(MACHADO GUERREIRO)",10, 7),
		(61,"CHLAMYDIA PNEUMONIE(IGG)",10),
		(62,"CHLAMYDIA PNEUMONIE(IGM)",10),
		(63,"CHLAMYDIAS TRACHOMATIS(IGG)",10),
		(64,"CHLAMYDIAS TRACHOMATIS(IGM)",10),
		(65,"CITOMEGALOVIRUS(IGG)",10),
		(66,"CITOMEGALOVIRUS(IGM)",10),
		(67,"CITRATO EN ORINA 24H",10, 6),
		(68,"CITRATO EN ORINA CASUAL",10, 6),
		(69,"CK-MB(ISOENZIMA CREATINQUINASA)",0, 2),
		(70,"CK-TOTAL(CREATINQUINASA)",0, 2),
		(71,"CLORO",0, 1),
		(72,"COLESTEROL TOTAL",2, 1),
		(73,"COMPLEMENTO C3",10),
		(74,"COMPLEMENTO C4",10),
		(75,"CORTICOTROPINA(ACTH)",20),
		(76,"CORTISOL 4:00 PM",10, 8),
		(77,"CORTISOL BASAL",10, 8),
		(78,"CORTISOL EN ORINA 24H",10, 6),
		(79,"CREATININA",2, 1),
		(80,"CREATININA EN ORINA CASUAL",2, 6),
		(81,"CREATININA EN ORINA 24H",2, 6),
		(82,"CRIOAGLUTININA",2),
		(83,"CURVA DE TOLERANCIA GLUCOSADA(2 TOMA)",4, 12),
		(84,"CURVA DE TOLERANCIA GLUCOSADA(3 TOMA)",6, 12),
		(85,"CURVA DE TOLERANCIA GLUCOSADA(4 TOMA)",8, 12),
		(86,"DENGUE",3, 7),
		(87,"DEPURACION DE ACIDO URICO EN 24H",3, 6),
		(88,"DEPURACION DE CREATININA EN 24H",3, 6),
		(89,"DEPURACION DE UREA EN 24H",3, 6),
		(90,"LDH(DESHIDROGENASA LACTICA)",2, 2),
		(91,"DHEAS",10, 8),
		(92,"DIGOXINA",15, 9),
		(93,"DIMERO D",20, 1),
		(94,"DREPANOCITOS(CEDULAS FALCIFORMES)",4, 4),
		(95,"ELECTROLITOS SERICOS(NA+,K+,F+)",6, 1),
		(96,"ELECTROLITOS URINARIOS(NA,K,CL)",6, 6),
		(97,"ELECTROLITOS URINARIOS EN 24H",6, 6),
		(98,"EPSTEIN BARR VIRUS(EBV) IGG",10),
		(99,"EPSTEIN BARR VIRUS(EBV) IGM",10),
		(100,"ESTRADIOL",10, 8),
		(101,"LEOUCOGRAMA Y EX.GRAL.",2, 3),
		(102,"FACTOR REMATOIDE CUANTITATIVO",3, 7),
		(103,"FERRITINA",5),
		(104,"FIBRINOGENO",2, 5),
		(105,"FOLATO(ACIDO FOLICO)",14, 1),
		(106,"FOSFATASA ALCALINA",2, 2),
		(107,"FOSFORO EN ORINA 24H",2, 6),
		(108,"FOSFORO EN ORINA CASUAL",2, 6),
		(109,"FOSFORO SERICO",2, 1),
		(110,"FROTIS SANGUINEO",3, 4),
		(111,"FTA ABS",10, 7),
		(112,"GAMMA GLUTAMIL TRANSFERRA(GGT)",3, 1),
		(113,"GGT",3, 1),
		(114,"GLICEMIA",2, 1),
		(115,"GLICEMIA 120MIN",2, 1),
		(116,"GLICEMIA 30MIN",2, 1),
		(117,"GLICEMIA 60MIN",2, 1),
		(118,"GLICEMIA 90MIN",2, 1),
		(119,"GLICEMIA BASAL",2, 1),
		(120,"GLICEMIA POST - PANDRIAL",2, 1),
		(216,"GOTA GRUESA", 5, 4),
		(121,"GRUPO SANGUÍNEO Y FACTOR RH(TIPIAJE)",2, 4),
		(122,"H.I.V",2, 7),
		(123,"HCG EN SANGRE",2, 8),
		(124,"HECES, EXAMEN GENERAL",2, 3),
		(125,"HELICOBACTER PYLORI EN HECES",10, 3),
		(126,"HELICOBACTER PYLORI(IGG)",10, 7),
		(127,"HELICOBACTER PYLORI(IGM)",10, 7),
		(128,"HEMATOLOGIA COMPLETA",3, 4),
		(129,"HEMOGLOBINA GLICOLISADA A1C",10, 1),
		(130,"HEPATITIS A(IGM)",4, 7),
		(131,"HEPATITIS A(IGG)",0, 7),
		(132,"HEPATITIS B",3, 7),
		(133,"HEPATITIS C",3, 7),
		(134,"HERPES VIRUS",20),
		(135,"HIERRO SERICO",5, 1),
		(136,"HOMA - IR",2, 1),
		(137,"HOMOCISTEINA",20),
		(138,"HORMONA ANTIMULLERIANA",15, 8),
		(139,"FSH(HORMONA FOLICO ESTIMULANTE)",8, 8),
		(140,"LH(HORMONA LUTEINIZANTE)",8, 8),
		(141,"INMUNOGLOBULINA A",10),
		(142,"INMUNOGLOBULINA A SECRETORA(IGA)",10),
		(143,"INMUNOGLOBULINA E(IGE)",10),
		(144,"INMUNOGLOBULINA G(IGG)",10),
		(145,"INMUNOGLOBULINA M(IGM)",10),
		(146,"INR",2, 5),
		(147,"INSULINA 120MIN",5, 8),
		(148,"INSULINA 30MIN",5, 8),
		(149,"INSULINA 60MIN",5, 8),
		(150,"INSULINA 90MIN",5, 8),
		(151,"INSULINA BASAL",5, 8),
		(152,"INSULINA POST - PANDRIAL",5, 8),
		(153,"LIPASA",0, 2),
		(154,"MAGNESIO",2, 1),
		(155,"MAGNESIO EN ORINA 24H",2, 6),
		(156,"MAGNESIO EN ORINA CASUAL",2, 6),
		(157,"MICROPLASMA PNEUMONIAE(IGG)",10),
		(158,"MICROPLASMA PNEUMONIAE(IGM)",10),
		(159,"MICROALBUMINURIA",5, 6),
		(160,"MICROALBUMINURIA EN ORINA 24H",5, 6),
		(161,"ORINA, EXAMEN GENERAL",2, 6),
		(162,"OXALATO EN ORINA 24H",10, 6),
		(163,"OXALATO EN ORINA CASUAL",10, 6),
		(164,"PTH(PARATHORMONAS)",20, 8),
		(165,"PEPTIDO C",0),
		(166,"PERFIL LIPIDICO",4, 1),
		(167,"PH EN HECES",2, 3),
		(168,"POTASIO(K)",0, 1),
		(169,"POTASIO EN ORINA PARCIAL",0, 6),
		(170,"PROCALCITONINA",10),
		(171,"PROGESTERONA",10, 8),
		(172,"PROLACTINA",10, 8),
		(173,"PROTEINA C REACTIVA CUANTIFICADO",3, 7),
		(174,"PROTEINAS TOTALES",3, 1),
		(175,"PROTEINAS TOTALES EN LIQUIDO ASCITICO",0, 1),
		(176,"PROTEINURIA EN ORINA 24H",2, 6),
		(177,"PROTEINURIA ORINA 12H",2, 6),
		(178,"PROTEINURIA EN ORINA PARCIAL",2, 6),
		(179,"RA TEST",3, 7),
		(180,"RELACION ALBULIMIA/CREATININA",2, 13),
		(181,"RELACION FOSFORO/CREATININA",2, 13),
		(182,"RELACION MAGNESIO/CREATININA",2, 13),
		(183,"RELACION ACIDO URICO/CREATININA",2, 13),
		(184,"RELACION PROTEINA/CREATININA",2, 13),
		(185,"RELACION CITRATO/CREATININA",15, 13),
		(186,"RELACION CALCIO/CREATININA",2, 13),
		(187,"RUBEOLA(IGG)",10),
		(188,"RUBEOLA(IGM)",10),
		(189,"SANGRE OCULTA",2, 3),
		(190,"SEROLOGIA PARA HONGOS",10),
		(191,"SEROLOGIA PARA MYCOPLASMA",20),
		(192,"T3 LIBRE",5, 8),
		(193,"T4 LIBRE",5, 8),
		(194,"TESTOSTERONA LIBRE",10, 8),
		(195,"TESTOSTERONA TOTAL",10, 8),
		(196,"TIEMPO DE PROTROMBINA(P.T)",2.5, 5),
		(197,"TIEMPO PARCIAL DE TROMBOPL.(P.T.T)",2.5, 5),
		(198,"TIROGLOBULINAS",10, 8),
		(199,"TOXOPLASMA(IGM)",5, 7),
		(200,"TOXOPLASMA(IGG)",5, 7),
		(201,"TRANSAMINASA OXALACETICA(TGO)",2, 2),
		(202,"TRANSAMINASA PIRUVICA(TGP)",2, 2),
		(203,"TRANSAFERRINA",8),
		(204,"TRANSFERRINA EN HECES",0, 3),
		(205,"TRIGLICERIDOS",2, 1),
		(206,"TROPONINA I",0),
		(207,"TROPONINA I CUALITATIVA",0),
		(208,"TSHUSHORMONA ESTIMULANTE DEL TIROIDES",5, 8),
		(209,"UREA",2, 1),
		(210,"UREA EN ORINA 24H",2, 6),
		(211,"UREA EN ORINA CASUAL",2, 6),
		(212,"V.D.R.L.",2, 7),
		(213,"VARICELA(IGG)",0, 7),
		(214,"VARICELA(IGM)",0, 7),
		(215,"VELOCIDAD DE SEDIMENTACION GLOBULAR(V.S.G)",2, 4)
	]
		for i in data:
			try:
				cursor.execute("INSERT INTO INFOEXAMENES VALUES(?, ?, ?, ?)", i,)
			except: #completar automaticamente los que no tienen grupo
				cursor.execute("INSERT INTO INFOEXAMENES VALUES(?, ?, ?, ?)", (i[0], i[1],i[2], 11,))
	else:
		pass

	bbdd.commit()
	bbdd.close()

def examenesHijo():
	#codigoPadre #codigoHijo #descripcion #unidad #valor referencia

	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS EXAMENESHIJO (CODIGOEXAMENPADRE INTEGER, CODIGOEXAMENHIJO INTEGER, DESCRIPCION TEXT, UNIDADMEDICION TEXT, VALORREFERENCIA TEXT)")

	cursor.execute("SELECT * FROM EXAMENESHIJO")
	validate = cursor.fetchall()

	if validate == []:
		data = [
			(1, 1, "HIERRO", "mg/dl", "50 - 175"),
			(1, 2, "TRANSFERRINA", "g/dl", "200 - 360"),
			(1, 3, "% SATURACION", " ", " "),
			(2, 1, "17-HIDROXI-PROGESTERONA", "ng/L", "Fase Folic: 0.20 - 1.30\n Fase Lutea: 1.0 - 4.5\n Menopausia: 0.10 - 1-20"),
			(3, 1, "17-HIDROXI-ANDROSTENEDIONA", "ug/ml", "110 - 190"),
			(4, 1, "AC. B2 GLICOPROTEINA IGG", "UI/ml", "POSITIVO MAYORA 10"),
			(5, 1, "AC. B2 GLICOPROTEINA IGM", "UI/ml", "POSITIVO MAYOR A 8.00"),
			(6, 1, "AC. URICO", "mg/dl", "1.5 - 6.1"),
			(7, 1, "VOLUMEN DE ORINA", "ml/24", "ml/24"),
			(7, 2, "AC. URICO DE LA MUESTRA", "mg/dl", "mg/dl"),
			(7, 3, "AC. URICO ORINA 24 HORAS", "mg/24", "mg/24"),
			(8, 1, "AC. URICO EN ORINA CASUAL", "mg/dl", "7-50"),
			(9, 1, "ACIDO ANTI-DNA", "UI/ml", "NEGATIVO: 0.00 - 100.0\n POSITIVO MAYOR A 100.0"),
			(10, 1, "ACIDO FOLICO", "ng/ml", "3.0 - 17.0"),
			(11, 1, "ACTH", "ng/ml", "5 - 17"),
			(12, 1, "ADENOVIRUS (HECES)", " ", " "),
			(13, 1, "ALFA-FETOPROTEINA (AFP)", "UI/ml", "0.00 - 15.00"),
			(14, 1, "AMILASA SERICA", "UA/dL", "Normal: <120\n Pancreatitis Aguda: 300 a 12.000\n Pancreatitis Cronica Hasta 200\n Parotiditis: 200 a 350\n Parotiditis con complicacion\n pancreatica: Mas de 350"),
			(15, 1, "AMONIO", " ", " "),
			(16, 1, "AMONIO POST PANDRIAL", " ", " "),
			(17, 1, "ANCA", " ", " "),
			(18, 1, "ANDROSTENEIDOA", " ", " "),
			(19, 1, "ANTI CARCINOEMBRIONARIO (CEA)", " ", " "),
			(20, 1, "ANTI CCP (ANTIPEPTIDO CITRUNILADO)", "UI/ml", "HASTA 25"),
			(21, 1, "ANTI E", " ", " "),
			(22, 1, "ANTI JO-1", "UI/mL", "NEGATIVO: 0.00 - 12.00\n INDETERMINADO: 12.01 - 18.00\n POSITIVO MAYOR A 18.01"),
			(23, 1, "ANTI SCL 70", "UI/mL", "NEGATIVO: 0.00 - 10.00\n INDETERMINADO: 10.01 - 20.00\n POSITIVO MAYOR DE 20.01"),
			(24, 1, "ANTICORE", " ", " "),
			(25, 1, "ANTI-CORE IGG", " ", " "),
			(26, 1, "ANTI-CORE IGM", " ", " "),
			(27, 1, "ANTICUERPO ANTI B2 GLICOPROTEINAS IGG", "UI/mL", "POSITIVO MAYOR A 12.05"),
			(28, 1, "AC. B2 GLICOPROTINA IGM", "UI/mL", "POSITIVO MAYOR A 8.00"),
			(29, 1, "ANTICUERPOS ANTI - RO(SS-A)", "UI/mL", " "),
			(30, 1, "ANTICUERPOS ANTI - LA(SS-B)", "UI/mL", " "),
			(31, 1, "ANTICUERPOS ANTICARDIOLIPINAS IGG", "UI/mL", "POSITIVO MAYOR A 8"),
			(32, 1, "ANTICUERPOS ANTICARDIOLIPINAS IGM", "UI/mL", "POSITIVO MAYOR A 8"),
			(33, 1, "ANTICUERPOS ANTIFOSFOLIPIDOS", " ", " "),
			(34, 1, "ANTICUERPOS ANTINUCLEARES(ANA)", "UI/mL", "POSITIVO MAYOR DE 0.9"),
			(35, 1, "ANTI MICROSOMALES", "IU/mL", "NEGATIVO: 0.00 - 11.90\n INDETERMINADO: 12.00 - 18.00\n POSITIVO: MAYOR A 18.00"),
			(35, 2, "AC. ANTI-PEROX.TIROIDEA (ANTI-TPO)", "IU/mL", "NEGATIVO: 0.00 - 11.90\n INDETERMINADO: 12.00 - 18.00\n POSITIVO: MAYOR A 18.00"),
			(35, 3, "AC. ANTI-TIROGLOBULINA (ANTI-TG)", "IU/mL", "NEGATIVO: 0.00 - 11.90\n INDETERMINADO: 12.00 - 18.00\n POSITIVO: MAYOR A 18.00"),
			(36, 1, "ANTI-DNA", "UI/mL", "POSITIVO MAYOR A 0.9"),
			(37, 1, "ANTIGENO PROSTATICO(PSA)", "ng/mL", "0.0 - 4.0"),
			(38, 1, "ANTIGENO PROSTATICO(LIBRE)", "ng/mL", "0.0 - 0.9"),
			(39, 1, "S. TYPHI(H)", " ", " "),
			(39, 2, "S. PARATYPHI(AO)", " ", " "),
			(39, 3, "BRUCELLAS ABORTUS", " ", " "),
			(39, 4, "S. PARATYPHI(AH)", " ", " "),
			(39, 5, "PROTEUS OX-19", " ", " "),
			(39, 6, "S. PARATYPHI(BH)", " ", " "),
			(39, 7, "S. PARATYPHI(O)", " ", " "),
			(39, 8, "S. PARATYPHI(BO)", " ", " "),
			(39, 9, "S. TYPHI(O)", " ", " "),
			(39, 10, "S. PARATYPHI(CH)", " ", " "),
			(39, 11, "S. PARATYPHI(CO)", " ", " "),
			(40, 1, "ANTIMICROSOMALES", "IU/mL", "POSITIVO: MAYOR A 40"),
			(41, 1, "ANTIMITOCONDRIALES", "INDEX", " "),
			(42, 1, "ANTIPEROXIDASA(TPO)", " ", "POSITIVO: MAYOR DE 40"),
			(43, 1, "ANTITIROGLOBULINA", "IU/mL", "Hasta 150"),
			(45, 1, "ASTO (ANTIESTREPTOLISINA 0", "IU/ml", "0 - 200"),
			(46, 1, "AZUCARES REDUCTORES", "", ""),
			(47, 1, "BETA 2 MICROGLOBULINA", "ng/ml", "0.82 - 2.20"),
			(48, 1, "BHCG", "UI/L", "Mujeres Cíclicas HASTA 5.0\n4 - 5 SEMANAS 1500 - 23000\n5 - 6 SEMANAS 2400 - 135300\n6 - 7 SEMANAS 10500 - 161000\n7 - 8 SEMANAS 18000 - 209000\n8 - 9 SEMANAS 37500 - 218000\n9 - 10 SEMANAS 42800 - 219000 \n10 - 11 SEMANAS 33700 - 218700\n11 - 12 SEMANAS 21800 - 193200\n12 - 13 SEMANAS 20300 - 166100\n13 - 14 SEMANAS 15400 - 190000"),
			(49, 1, "BILIRRUBINA TOTAL", "mg/dl", "HASTA 1.2"),
			(49, 2, "BILIRRUBINA DIRECTA", "mg/dl", "HASTA 0.3 mg/dl"),
			(49, 3, "BILIRRUBINA INDIRECTA", " ", "HASTA 1.0 mg/dl"),
			(50, 1, "CA - 125", "UI/mL", "0.00 - 35.00"),
			(51, 1, "CA - 15 - 3", "UI/mL", "0.00 - 31.00"),
			(52, 1, "CA - 19 - 9", "UI/mL", "0.00 - 35.00"),
			(53, 1, "VOLUMEN URINARIO", "ml/24h", " "),
			(53, 2, "PH", " ", " "),
			(53, 3, "DENSIDAD", " ", " "),
			(53, 4, "CALCIO DE LA MUESTRA", "mg/dl", " "),
			(53, 5, "CALCIO ORINA 24 HORAS", "mg/24h", " "),
			(54, 1, "CALCIO EN ORINA PARCIAL", "mg/dl", "2 - 17"),
			(55, 1, "CALCIO SERICO", "mg/dl", "Adultos jovenes: 8.7 - 10.7\n Adultos de mas edad: 8.5 - 10.5\nRecien Nacidos: 7.8 - 11.2\nNiños: 9.0 - 11.0"),
			(56, 1, "CARBAMANZEPINA", "ng/ml", "VALORES NORMALES PARA\nPACIENTES CON TRATAMIENTO TERAPEUTICO\n8 - 12"),
			(57, 1, "CARGA GLYCOLAB", " ", " "),
			(58, 1, "CELULAS L.E.", " ", " "),
			(59, 1, "CH-50", "UH/mL", "150 - 250"),
			(60, 1, "CHAGAS (MANCHADO GUERREIRO)", " ", " "),
			(61, 1, "CHLAMYDIA PNEUMONIE (IGG)", "UI/mL", "NEGATIVO: 0.00 - 1.50\nPOSITIVO MAYOR DE 1.51"),
			(62, 1, "CHLAMYDIA PNEUMONIE (IGM)", "UI/mL", "NEGATIVO: 0.00 - 9.00\nPOSITIVO MAYOR DE 9.00"),
			(63, 1, "CHLAMYDIA TRACHOMATIS (IGG)", "INDEX", "NEGATIVO MENOR DE 0.9\nPOSITIVO MAYOR DE 0.9"),
			(64, 1, "CHLAMYDIAS TRACHOMATIS (IGM)", "INDEX", "NEGATIVO MENOR DE 0.9\nPOSITIVO MAYOR DE 0.9"),
			(65, 1, "CITOMEGALOVIRUS (IGG)", "UI/mL", "POSITIVO MAYOR A 1.0"),
			(66, 1, "CITOMEGALOVIRUS (IGM)", "UI/mL", "POSITIVO MAYOR A 1.0"),
			(67, 1, "CITRATO EN ORINA 24H", "mg/24h", "320 - 1240"),
			(68, 1, "CITRATO EN ORINA CASUAL", "mg/dl", "12 - 45"),
			(69, 1, "CK - MB (ISOENZIMA CREATINQUINASA)", "U/L", "24 - 170"),
			(70, 1, "CK - TOTAL (CREATINQUINASA)", "U/L", "HASTA 170"),
			(71, 1, "CLORO", "meq/lt", "98 - 108"),
			(72, 1, "COLESTEROL TOTAL", "mg/dl", "Deseable: Menor de 200 mg/dl\nModeradamente alto: 200 - 239 mg/dl\nElevado: Mayor o igual 240 mg/dl"),
			(73, 1, "COMPLEMENTO C3", "mg/dl", "60 - 180"),
			(74, 1, "COMPLEMENTO C4", "mg/dl", "12.9 - 39.2"),
			(75, 1, "CORTICOTROPINA (ACTH)", "ng/ml", "25 - 100"),
			(76, 1, "CORTISOL 4:00 PM", "ug/dl", "30 - 150 ug/dl"),
			(77, 1, "CORTISOL BASAL", "ng/mL", "50 - 230 ng/ml"),
			(78, 1, "CORTISOL EN ORINA 24 HORAS", "mg/24h", "NIÑOS: 15 - 50\nADULTOS: 30 - 100"),
			(79, 1, "CREATININA", "mg/dl", "0.5 - 1.4\nNiñas: 0.35 + (0.033 x edad en años)"),
			(80, 1, "CREATININA EN ORINA CASUAL", "mg/dl", "30 - 125"),
			(81, 1, "VOLUMEN", "mg/24h", " "),
			(81, 2, "CREATININA DE LA MUESTRA", " ", " "),
			(81, 3, "CREATININA ORINA 24HORAS", "ml/24", " "),
			(82, 1, "CRIOAGLUTININA", " ", " "),
			(83, 1, "GLICEMIA BASAL", "mg/dl", "70 - 110"),
			(83, 2, "60 MIN", "mg/dl", " "),
			(83, 3, "120 MIN", "mg/dl", " "),
			(84, 1, "GLICEMIA BASAL", "mg/dl", "70 - 110"),
			(84, 2, "30 MIN", "mg/dl", "70 - 150"),
			(84, 3, "60 MIN", "mg/dl", " "),
			(84, 4, "120 MIN", "mg/dl", "140 - 200"),
			(85, 1, "GLICEMIA BASAL", "mg/dl", "70 - 110"),
			(85, 2, "1 HORA", "mg/dl", "ADULTOS: 110 - 170 mg/dl NIÑOS: < 140 mg/dl"),
			(85, 3, "2 HORA", "mg/dl", "ADULTOS: 70 -120 mg/dl NIÑOS: < 140 mg/dl"),
			(85, 4, "3 HORA", "mg/dl", "ADUTLOS: 70 -120 mg/dl"),
			(85, 5, "4 HORA", "mg/dl", " "),
			(86, 1, "ANTICUERPOS IGM ANTI - DENGUE", " ", " "),
			(86, 2, "ANTICUERPOS IGG ANTI - DENGUE", " ", " "),
			(87, 1, "VOLUMEN EN 24 HORAS", " ", " "),
			(87, 2, "VOLUMEN MINUTO", "ml/min", " "),
			(87, 3, "ACIDO URICO SERICO", "mg/dl", "2.5 - 7.7"),
			(87, 4, "AC. URICO EN ORINA", "mg/dl", " "),
			(87, 5, "RESULTADO DE LA DEPURACION", "ml/min", " "),
			(88, 1, "CREATININA EN SANGRE", " ", " "),
			(88, 2, "CREATININA EN ORINA", "mg/24h", " "),
			(88, 3, "DEPURACION DE CREATININA", "ml/min", "40 - 130"),
			(88, 4, "VOLUMEN TOTAL", "ml/24", " "),
			(88, 5, "VOLUMEN MINUTO", "ml/min", " "),
			(88, 6, "PH", " ", " "),
			(88, 7, "DENSIDAD", " ", " "),
			(89, 1, "VOLUMEN EN 24 HORAS", "mts", " "),
			(89, 2, "PESO", "Kg", " "),
			(89, 3, "TALLA", "ml", " "),
			(89, 4, "SUPERFICIE CORPORAL", "m2/sc", " "),
			(89, 5, "UREA SERICA", "mg/dl", " "),
			(89, 6, "UREA EN ORINA", "mg/dl", " "),
			(89, 7, "RESULTADO DE LA DEPURACION", "ml/min", " "),
			(90, 1, "DESHIDROGENASA LACTICA (LDH)", "IU/L", "80 - 285"),
			(91, 1, "DHEAS", "ug/mL", "0.7 - 3.90"),
			(92, 1, "DIGOXINA", "ng/ml", "0.8 - 12"),
			(93, 1, "DIMERO D", "ug/mL", "Menor a 0.5"),
			(94, 1, "DREPANOCITOS (CEDULAS FALCIFORMES)", " ", " "),
			(95, 1, "SODIO (NA)", "mmol/l", "135.0 - 155.0 mmol/l"),
			(95, 2, "POTASIO (K)", "mmol/l", "3.60 - 5.50"),
			(95, 3, "CLORO (CL)", "mmol/l", "98 - 108 mmol/l"),
			(96, 1, "SODIO (NA)", "mEq/l", " "),
			(96, 2, "POTASIO (K)", "mEq/l", " "),
			(96, 3, "CLORO (CL)", "mEq/l", " "),
			(97, 1, "SODIO (NA)", "mEq/24h", "80 - 200"),
			(97, 2, "POTASIO (K)", "mEq/24h", "25 - 75"),
			(97, 3, "CLORO (CL)", "mEq/24h", "116 - 130"),
			(98, 1, "EPSTEIN BARR VIRUS(EBV) IGG", "UI/mL", "POSITIVO: MAYOR A 1.0"),
			(99, 1, "EPSTEIN BARR VIRUS(EBV) IGM", "UI/mL", "POSITIVO: MAYOR A 1.0"),
			(100, 1, "ESTRADIOL", "pg/mL", "FASE FOLIC: 100 - 400\nFASE LUTEA: 60 - 150\nMENOPAUSIA: <18"),
			(101, 1, "EX.GRAL. Y LEOUCOGRAMA", " ", " "),
			(102, 1, "FACTOR REUMAOTOIDE CUANTITATIVO", "IU/mL", "0.00 - 8.00"),
			(103, 1, "FERRITINA", "ng/mL", "ADULTOS: 10 - 124\nNIÑOS: 7 - 140\nRECIEN NACIDOS: 22 - 220"),
			(104, 1, "FIBRINOGENO", "mg/dl", "200 - 400"),
			(105, 1, "FOLATO (ACIDO FOLICO)", "ng/ml", "2 - 10"),
			(106, 1, "FOSFATASA ALCALINA", "U/L", "Niños 1 - 12 años: Hasta 596\nNiños 13 - 17 años: Hasta 367\nAdultos: 30 - 170"),
			(107, 1, "VOLUMEN TOTAL", "ml/24h", " "),
			(107, 2, "FOSFORO DE LA MUESTRA", " ", " "),
			(107, 3, "FOSFORO EN ORINA 24 HORAS", " ", " "),
			(108, 1, "FOSFORO EN ORINA CASUAL", "mg/dl", "0 - 60"),
			(109, 1, "FOSFORO SERICO","mg/dl", "ADULTOS: 2.5 - 4.8\nNIÑOS: 4.0 - 7.0(1er año de vida)"),
			(110, 1, "GLOBULOS ROJOS", " ", " "),
			(110, 2, "GLOBULOS BLANCOS", " ", " "),
			(110, 3, "PLAQUETAS", " ", " "),
			(111, 1, "FTA ABS", " ", " "),
			(112, 1, "GAMMA GLUTAMIL TRANSFERRA(GGT)", "U/L", "7 - 38"),
			(113, 1, "GGT", "U/L", "HOMBRES: 0 - 55\nMUJERES: 0 - 38"),
			(114, 1, "GLICEMIA", "mg/dL", "70 - 105"),
			(115, 1, "GLICEMIA 120 MIN", "mg/dl", "Menor a 140"),
			(116, 1, "GLICEMIA 30 MIN", "mg/dl", "120 - 170"),
			(117, 1, "GLICEMIA 60 MIN", "mg/dl", "Menor a 200"),
			(118, 1, "GLICEMIA 90 MIN", "mg/dl", "MENOR A 200"),
			(119, 1, "GLICEMIA BASAL", "mg/dl", "Basal: 60 a 100"),
			(120, 1, "GLICEMIA POST - PANDRIAL", "mg/dl", "1 hora: menos de 200 mg/dl\n2 horas: menos de 140 mg/dl"),
			(121, 1, "GRUPO SANGUÍNEO", " ", " "),
			(121, 2, "FACTOR RH", " ", " "),
			(122, 1, "H.I.V", " ", " "),
			(123, 1, "HCG EN SANGRE", " ", " "),
			(124, 1, "COLOR", " ", " "),
			(124, 2, "CONSISTENCIA", " ", " "),
			(124, 3, "ASPECTO", " ", " "),
			(124, 4, "MOCO", " ", " "),
			(124, 5, "SANGRE APARENTE", " ", " "),
			(124, 6, "REACCION", " ", " "),
			(124, 7, "OBSERVACIONES", " ", " "),
			(125, 1, "HELICOBACTER PYLORI EN HECES", " ", " "),
			(126, 1, "HELICOBACTER PYLORI IGG", "UI/mL", "POSITIVO MAYOR A 1.0"),
			(127, 1, "HELICOBACTER PYLORI IGM", "UI/mL", "POSITIVO MAYOR A 1.0"),
			(128, 1, "HEMOGLOBINA", "g/dl", "11.0 - 16.5"),
			(128, 2, "GLOBULOS ROJOS", "cel/ul", "3.5 - 5.5x10*6"),
			(128, 3, "HEMATOCRITO", "%", "37 - 50%"),
			(128, 4, "VCM", "fl", "82.0 - 95.0"),
			(128, 5, "HCM", "pg", "27 - 31"),
			(128, 6, "CHCN", "g/dl", "32.0 - 36.0"),
			(128, 7, "LEUCOCITOS", "cel/ul", "4.5 - 10.5x10*3"),
			(128, 8, "NEUTROFILOS", "%", " "),
			(128, 9, "LINFOCITOS", "%", " "),
			(128, 10, "EOSINOFILOS", "%", " "),
			(128, 11, "PLAQUETAS", "cel/ul", "150 - 350x10*3"),
			(128, 12, "OBSERVACIONES", " ", " "),
			(129, 1, "HEMOGLOBINA GLICOSILADA A1C", "%", "4.00 - 6.00"),
			(130, 1, "ANTICUERPOS IGM ANTI - HEPATITIS A", " ", " "),
			(131, 1, "HEPATITIS A IGG", " ", " "),
			(132, 1, "ANTIGENO DE SUPERFICIE", " ", " "),
			(132, 2, "ANTICORE", " ", " "),
			(133, 1, "HEPATITIS C", " ", " "),
			(134, 1, "IGM HERPES TIPO I", "U/L", "POSITIVO MAYOR A 1.0"),
			(134, 2, "IGG HERPES TIPO I", "U/L", "POSITIVO MAYOR A 1.0"),
			(134, 3, "IGM HERPES TIPO II", "U/L", "POSITIVO MAYOR A 1.0"),
			(134, 4, "IGG HERPES TIPO II", "U/L", "POSITIVO MAYOR A 1.0"),
			(135, 1, "HIERRO SERICO", "Ug/dl", "50 - 170"),
			(136, 1, "HOMA - IR", " ", "HASTA 2.5"),
			(137, 1, "", "", ""),
			(138, 1, "", "", ""),
			(139, 1, "", "", ""),
			(140, 1, "HORMONA LUTEINIZANTE (LH)", "mlU/mL", "PRE-PUBERTAD: 0.7 - 2.3\nFASE FOLIC: 1.5 - 15\nFASE OVULATORIA: 21.9 - 56.6\nFASE LUTEA: 0.61 - 16.3\nMENOPAUSIA: 14.2 - 52.3"),
			(141, 1, "", "", ""),
			(142, 1, "", "", ""),
			(143, 1, "", "", ""),
			(144, 1, "", "", ""),
			(145, 1, "INMUNOGLOBULINA M (IGM)", "mg/dl", "30 - 230"),
			(146, 1, "INR", " ", " "),
			(147, 1, "INSULINA 120MIN", "ulU/mL", "< 60"),
			(148, 1, "INSULINA 30 MIN", "mUI/ml", "12.5 - 116"),
			(149, 1, "INSULINA 60 MIN", "mUI/ml", " "),
			(150, 1, "INSULINA 90 MIN", "mUI/ml", " "),
			(151, 1, "INSULINA BASAL", "mUI/ml", " "),
			(152, 1, "INSULINA POST - PADNRIAL", "mUI/ml", " "),
			(153, 1, "LIPASA", "UI/L", "10 - 140"),
   			(154, 1, "MAGNESIO","mg/dL", ""),
			(157, 1, "MICROPLASMA PNEUMONIAE (IGG)", "UI/mL", "NEGATIVO: 0.01 - 18.00\nPOSITIVO MAYOR A 18.00"),
			(158, 1, "MICROPLASMA PNEUMONIAE (IGM)", "UI/mL", "NEGATIVO: 0.00 - 0.90\nPOSITIVO MAYOR A 0.90"),
			(161, 1, "COLOR", "", ""),
			(161, 2, "ASPECTO", "", ""),
			(161, 3, "DENSIDAD", "", ""),
			(161, 4, "PH", "", ""),
			(161, 5, "PROTEINAS", "", ""),
			(161, 6, "HEMOGLOBINA", "", ""),
			(161, 7, "CETONAS", "", ""),
			(161, 8, "GLUCOSA", "", ""),
			(161, 9, "NITRITOS", "", ""),
			(161, 10, "UROBILINOGENO", "", ""),
			(161, 11, "PIG. BILIAR", "", ""),
			(161, 12, "CELULAS EPITELIALES", "", ""),
			(161, 13, "LEUCOCITOS", "", ""),
			(161, 14, "HEMATIES", "", ""),
			(161, 15, "BACTERIAS", "", ""),
			(161, 16, "MUCINA", "", ""),
			(161, 17, "OBSERVACIONES", "", ""),
			(162, 1, "OXALATO EN ORINA 24 HORAS", "mg/24h", "7 - 44"),
			(163, 1, "OXALATO EN ORINA CASUAL", "mg/dl", "4 - 20"),
			(165, 1, "PEPTIDO C", "ng/ml", "0.700 - 1.900"),
			(166, 1, "COLESTEROL TOTAL", "mg/dl", "140-200 mg/dl "),
			(166, 2, "TRIGLICERIDOS", "mg/dl", "40-160 mg/dl"),
			(166, 3, "HDL", "mg/dl", "45 - 70 mg/dl"),
			(166, 4, "LDL", "mg/dl", "menor a 100 mg/dl"),
			(166, 5, "VLDL", "mg/dl", " "),
			(166, 6, "REL. COLESTEROL/HDL", " ", "HASTA 5.0"),
			(166, 7, "REL.LDL/HDL", " ", "HASTA 3.0"),
			(168, 1, "POTASIO (K)", "mmol/L", "3.5 - 5.00"),
			(172, 1, "PROLACTINA", "ng/mL", "1.90 - 20.90"),
			(173, 1, "PROTEINA C REACTIVA CUANTIFICADO", "mg/dl", "0 - 5"),
			(174, 1, "PROTEINAS TOTALES", " ", "6.5 - 8.5"),
			(174, 2, "ALBUMINA", " ", "3.5 - 5.5"),
			(174, 3, "GLOBULINAS", " ", " "),
			(174, 4, "RE. ALBUMINA/GLOBULINAS", "", "1.2 - 2.2"),
			(176, 1, "VOLUMEN EM ORINA EN 24 HORAS", "ml/24horas", " "),
			(176, 2, "PROTEINURIA", "mg/dL", "0 - 6 mg/dl"),
			(176, 3, "PROTEINURIA EN 24 HORAS", "ml/24horas", " "),
			(176, 4, "PROTEINURIA CUALITATIVA", " ", " "),
			(177, 1, "VOLUMEN EN ORINA 12 HORAS", "ml/12horas", ""),
			(177, 2, "PROTEINURIA", "mg/dl", "0 - 6"),
			(177, 3, "PROTEINURIA EN 12 HORAS", " ", " "),
			(180, 1, "PROTEINURIA", " ", " "),
			(180, 2, "CREATINURIA", " ", " "),
			(180, 3, "RELACION PROT/CREAT", " ", " "),
			(181, 1, "FOSFORO", "mg/dl", "0 - 60"),
			(181, 2, "CREATININA", "mg/dl", "30 - 125"),
			(181, 3, "REL FOSF/CREAT", "mg/dl", "ADULTOS: 0.15 - 0.76\n0 - 2 AÑOS: 0.80 - 2.00\n3 - 5 AÑOS: 0.33 - 2.17\n5 - 7 AÑOS: 0.33 - 1.49\n7 - 10 AÑOS: 0.32 - 0.97\n10 - 14 AÑOS: 0.22"),
			(182, 1, "REL MAG/CREAT", " ", " "),
			(183, 1, "AC. URICO", "mg/dL", "7 - 50"),
			(183, 2, "CREATININA", "mg/24h", "30 - 125"),
			(183, 3, "REL. AC. URICO/CREAT", "mg/mg", "0.34 +- 0.10"),
			(184, 1, "PROTEINURIA", "mg/dl", "25"),
			(184, 2, "CREATININA", "mg/24h", "30 - 125"),
			(184, 3, "RELACION PROT/CREAT", "mg/dl", "FISIOLÓGICA <0.2\nLIGERA 0.2 - 1.2\nMODERADA 1.0 - 3.0"),
			(185, 1, "REL. CITRATO/CREATININA", "mg/dl", "0.2 - 0.4\nNIÑOS: MAYOR DE 0.38"),
			(186, 1, "CALCIO", "mg/dl", "2 - 17"),
			(186, 2, "CREATININA", " ", " "),
			(186, 3, "RELACION CAL/CREAT", "mg/mg", "0.12 +- 0.04"),
			(187, 1, "RUBEOLA IGG", "UI/mL", "NEGATIVO: 0.000 - 10.000"),
			(188, 1, "RUBEOLA IGM", "UI/mL", "NEGATIVO: 0.001 - 8.000\nPOSITIVO: MAYOR DE 8.000"),
			(192, 1, "T3", "pg/mL", "1.9 - 4.9"),
			(193, 1, "T4", "ng/dL", "0.65 - 2.2"),
			(194, 1, "TESTOSTERONA LIBRE", "pg/ml", "FASE FOLOCULAR: 0.45 - 3.17\nFASE LUTEAL: 0.46 - 2.48\nMENOPAUSIA: 0.10 - 1.73"),
			(195, 1, "TESTOSTERONA TOTAL", "pg/mL", "PRE-PUBERTAD: 0.1 - 0.3\nFASE FOLICULAR: 0.2 - 1.3\nFASE LUTEAL: 0.2 - 1.3\nPOST nMENOPAUSIA: 0.8 - 0.45"),
			(196, 1, "PT PACIENTE", "seg", " "),
			(196, 2, "PT CONTROL", "seg", " "),
			(196, 3, "RAZON", " ", "0.8 - 1.2"),
			(197, 1, "PTT PACIENTE", "seg", " "),
			(197, 2, "PTT CONTROL", "seg", " "),
			(197, 3, "DIFERENCIA", " ", "+-6"),
			(198, 1, "TIROGLOBULINAS", "ng/dl", "HASTA 52\nOPERADAS HASTA 5.0"),
			(199, 1, "TOXOPLASMA IGM", "UI/mL", "HASTA 1.0"),
			(200, 1, "TOXOPLASMA IGG", "UI/mL", "HASTA 1.0"),
			(201, 1, "TRANSAMINASA OXALACETICA (TGO)", "U/L", "5 - 34"),
			(202, 1, "TRANSAMINASA PIRUVICA (TGP)", "U/L", "HASTA 31"),
			(203, 1, "TRANSFERRINA", "g/L", "200 - 350"),
			(204, 1, "TRANSFERRINA EN HECES", " ", " "),
			(205, 1, "TRIGLICERIDOS", "mg/dl", "HASTA 150\n200 - 499 ALTO\nMAYOR A 500 MUY ALTO"),
			(206, 1, "TROPONINA I", "ng/ml", "0.000 - 0.028"),
			(207, 1, "TROPONINA I CUALITATIVA", " ", " "),
			(208, 1, "TSHusHORMONA ESTIMULANTE DEL TIROIDES", "mUI/L", "0.4 - 5.0"),
			(209, 1, "UREA", "mg/dl", "15 - 45"),
			(210, 1, "UREA EN ORINA 24H", "g/24h", "20 - 40"),
			(211, 1, "UREA EN ORINA CASUAL", "mg/dl", "12 - 2000"),
			(212, 1, "VDRL", " ", " "),
			(213, 1, "VARICELA IGG", " ", " "),
			(214, 1, "VARICELA IGM", " ", " "),
			(215, 1, "V.S.G", "mm/hora", "0 - 20")
		]
		a = 1
		for i in data:
			cursor.execute("INSERT INTO EXAMENESHIJO VALUES(?, ?, ?, ?, ?)", i,)
	else:
		pass

	bbdd.commit()
	bbdd.close()

def usuario():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOS (CODIGOUSUARIO INTEGER PRIMARY KEY AUTOINCREMENT, CEDULAUSUARIO INTEGER, NOMBREUSUARIO TEXT, APELLIDOUSUARIO TEXT, USUARIOTELEFONO TEXT, CONTRASEÑAUSUARIO TEXT, NIVELDEPERMISOS TEXT)")

		cursor.execute("SELECT * FROM USUARIOS")

		validate = cursor.fetchall()

		if validate == []:
            #password = 1234
			data = [1, 123456789, "Admin", "Admin", "04248570292", "bd18e9cc79b4eb06d9ba8a3bd95fd8e6c1b8e3315abf40d9b000e2f21582bd6b671ed9e0093fa790f159e53303631ddaafbcad0867ca206df6bae206f955404dd404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176b6db28512f2e000b9d04fba5133e8b1c6e8df59db3a8ab9d60be4b97cc9e81db", "Admin"]
			cursor.execute("INSERT INTO USUARIOS VALUES(?,?,?,?,?,?,?)", data,)
		else:
			pass
		bd.commit()

def factura():
	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	#(1, 25, 5, '2022-05-01', '13:41:35', 10, 47, 0, 4.7, 19, '\n', '0')
	cursor.execute("CREATE TABLE IF NOT EXISTS FACTURA (CODIGOUSUARIO INTEGER, CODIGOFACTURA INTEGER, CODIGOPACIENTE INTEGER, FECHAFACTURA DATE, HORAFACTURA TIME, COSTOTOTAL NUMERIC, COSTOSUBTOTAL NUMERIC, DIFERENCIA NUMERIC, DESCUENTO NUMERIC, TASACAMBIARIADEDOLAR NUMERIC, CODIGOEXAMENESDEFACTURA INTEGER, NOTA TEXT, ANULADA TEXT)")

	bbdd.commit()
	bbdd.close()

def presupuesto():
	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS PRESUPUESTO (CODIGOUSUARIO INTEGER, CODIGOPRESUPUESTO INTEGER, CODIGOPACIENTE INTEGER, FECHAFPRESUPUESTO DATE, COSTOTOTAL NUMERIC, COSTOSUBTOTAL NUMERIC, DESCUENTO NUMERIC, TASACAMBIARIADEDOLAR NUMERIC, CODIGOEXAMENESDEPRESUPUESTO INTEGER)")

	bbdd.commit()
	bbdd.close()

def paciente():
	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS PACIENTES (CODIGOPACIENTE INTEGER PRIMARY KEY AUTOINCREMENT, CEDULA TEXT, NOMBRE TEXT, APELLIDO TEXT, EDAD TEXT, TELEFONO TEXT, DIRECCION TEXT)")

	bbdd.commit()
	bbdd.close()

def formasDePago():
	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS FORMASDEPAGO (CODIGOUSUARIO INTEGER, CODIGOFACTURA INTEGER, CODIGOPACIENTE INTEGER, CANTIDADPAGADAEFECTIVO NUMERIC, CANTIDADPAGADADIVISA NUMERIC, CANTIDADPAGADAPUNTO NUMERIC, CANTIDADPAGADAPAGOMOVIL NUMERIC)")

	bbdd.commit()
	bbdd.close()

def examenesDeFactura():
	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS EXAMENESDEFACTURA (CODIGOUSUARIO INTEGER, CODIGOFACTURA INTEGER, CODIGOEXAMEN INTEGER, NOMBREEXAMEN TEXT, CATIDADEXAMEN INTEGER, PRECIODOLARES NUMERIC, PRECIOBOLIVARES NUMERIC)")

	bbdd.commit()
	bbdd.close()

def resultados():
	bbdd = sqlite3.connect("bbdd/BBDD")
	cursor = bbdd.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS RESULTADOS (CODIGOUSUARIO INTEGER, CODIGOFACTURA INTEGER,  CODIGOEXAMENPADRE INTEGER, CODIGOEXAMENHIJO INTEGER, RESULTADO TEXT)")

	bbdd.commit()
	bbdd.close()

def perfilesExamenes():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS PERFILES (CODIGOPERFIL INTEGER, NOMBREPERFIL TEXT, CODIGOEXAMENESDELPERFIL INTEGER)")

		cursor.execute("SELECT * FROM PERFILES")
		validate = cursor.fetchall()

		if validate == []:
			data = [192, 193, 208]

			for i in data:
				cursor.execute("INSERT INTO PERFILES VALUES(?,?,?)", (1, "Pefil Tiroideo", i, ))
		else:
			pass

		bd.commit()

def usuarioActivo():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOACTIVO (CODIGOUSUARIOACTIVO INTEGER)")
		bd.commit()

def tazaCambiaria():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS TAZACAMBIARIA (TAZADELDIA NUMERIC)")

		cursor.execute("INSERT INTO TAZACAMBIARIA VALUES(?)", (4.7, ))
		bd.commit()

def resultadosEntregados():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS EXAMENESENTREGADOS (CODIGOUSUARIO INTEGER, CODIGOFACTURA INTEGER, FECHADEENTREGA TEXT, NOMBREPACIENTE TEXT, NOMBREQUERCOGIOLOSEXAMENES TEXT, CEDULAQUERECOGIOLOSEXAMENES TEXT, PARENTESCO TEXT, ESTADO TEXT)")

		bd.commit()

def infoLaboratorio():
	with sqlite3.connect("bbdd/BBDD") as bd:
		cursor = bd.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS INFOLABORATORIO (DIRECCION TEXT, BIOANALISTA TEXT, SERIALBIOANALISTA TEXT)")

		#INFO EJEMPLO
		cursor.execute("INSERT INTO INFOLABORATORIO VALUES(?,?,?)", ("AV. PRINCIPAL CRUCE CON AV. RAUL LEONI URB TRONCONAL III CLINICA ROTARIA\nBARCELONA. EDO. ANZOATEGUI", "LCDO DENISE HERNANDEZ", "MSDS 12018 CB 515"))

		bd.commit()

def createBBDD():
	infoExamenes()
	examenesHijo()
	usuario()
	paciente()
	factura()
	presupuesto()
	formasDePago()
	examenesDeFactura()
	resultados()
	perfilesExamenes()
	usuarioActivo()
	tazaCambiaria()
	resultadosEntregados()
	infoLaboratorio()

if __name__ == '__main__':
	createBBDD()
