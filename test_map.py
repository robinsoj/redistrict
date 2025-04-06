def createTestMap():
    test_map = {}

    #Apache County
    test_map['apache1'] = sorted(['apache5','apache2'])
    test_map['apache2'] = sorted(['apache6','apache1','apache3'])
    test_map['apache3'] = sorted(['apache7','apache2','apache4'])
    test_map['apache4'] = sorted(['apache8','apache3'])
    test_map['apache5'] = sorted(['apache9','apache1','apache6'])
    test_map['apache6'] = ['apache2','apache5','apache7','apache10']
    test_map['apache7'] = ['apache3','apache6','apache8','apache11']
    test_map['apache8'] = ['apache4','apache7','apache12']
    test_map['apache9'] = ['apache5','apache10','apache13']
    test_map['apache10'] = ['apache6','apache9','apache11','apache14']
    test_map['apache11'] = ['apache7','apache10','apache12','apache15']
    test_map['apache12'] = ['apache8','apache11','apache16']
    test_map['apache13'] = ['apache9','apache14','apache17']
    test_map['apache14'] = sorted(['apache18','apache13','apache10','apache15'])
    test_map['apache15'] = sorted(['apache19','apache14','apache11','apache16'])
    test_map['apache16'] = sorted(['apache20','apache15','apache12'])
    test_map['apache17'] = sorted(['apache21','apache13','apache18'])
    test_map['apache18'] = sorted(['apache22','apache17','apache14','apache19'])
    test_map['apache19'] = sorted(['apache23','apache18','apache15','apache20'])
    test_map['apache20'] = sorted(['apache24','apache19','apache16'])
    test_map['apache21'] = sorted(['apache25','apache17','apache22'])
    test_map['apache22'] = sorted(['apache26','apache21','apache18','apache23'])
    test_map['apache23'] = sorted(['apache27','apache22','apache19','apache24'])
    test_map['apache24'] = sorted(['apache28','apache23','apache20'])
    test_map['apache25'] = sorted(['apache29','apache21','apache26'])
    test_map['apache26'] = sorted(['apache30','apache25','apache22','apache27'])
    test_map['apache27'] = sorted(['apache31','apache26','apache23','apache28'])
    test_map['apache28'] = sorted(['apache32','apache27','apache24'])
    test_map['apache29'] = sorted(['apache33','apache25','apache30'])
    test_map['apache30'] = sorted(['apache34','apache29','apache26','apache31'])
    test_map['apache31'] = sorted(['apache35','apache30','apache27','apache32'])
    test_map['apache32'] = sorted(['apache36','apache31','apache28'])
    test_map['apache33'] = sorted(['apache37','apache29','apache34'])
    test_map['apache34'] = sorted(['apache38','apache33','apache30','apache35'])
    test_map['apache35'] = sorted(['apache39','apache34','apache31','apache36'])
    test_map['apache36'] = sorted(['apache40','apache35','apache32'])
    test_map['apache37'] = sorted(['apache41','apache33','apache38'])
    test_map['apache38'] = sorted(['apache42','apache37','apache34','apache39'])
    test_map['apache39'] = sorted(['apache43','apache38','apache35','apache40'])
    test_map['apache40'] = sorted(['apache44','apache39','apache36'])
    test_map['apache41'] = sorted(['apache37','apache42'])
    test_map['apache42'] = sorted(['apache41','apache38','apache43'])
    test_map['apache43'] = sorted(['apache42','apache39','apache44'])
    test_map['apache44'] = sorted(['apache43','apache40'])

    #Cochise County
    test_map['cochise1'] = ['cochise2','cochise8']
    test_map['cochise2'] = ['cochise1','cochise3','cochise9']
    test_map['cochise3'] = ['cochise2','cochise4','cochise10']
    test_map['cochise4'] = ['cochise3','cochise5','cochise11']
    test_map['cochise5'] = ['cochise4','cochise6','cochise12']
    test_map['cochise6'] = ['cochise5','cochise7','cochise13']
    test_map['cochise7'] = ['cochise6','cochise14']
    test_map['cochise8'] = ['cochise1','cochise9','cochise15']
    test_map['cochise9'] = ['cochise2','cochise8','cochise10','cochise16']
    test_map['cochise10'] = ['cochise3','cochise9','cochise11','cochise17']
    test_map['cochise11'] = ['cochise4','cochise10','cochise12','cochise18']
    test_map['cochise12'] = ['cochise5','cochise11','cochise13','cochise19']
    test_map['cochise13'] = ['cochise6','cochise12','cochise14','cochise20']
    test_map['cochise14'] = ['cochise7','cochise13','cochise21']
    test_map['cochise15'] = ['cochise8','cochise16','cochise22']
    test_map['cochise16'] = ['cochise9','cochise15','cochise17','cochise23']
    test_map['cochise17'] = ['cochise10','cochise16','cochise18','cochise24']
    test_map['cochise18'] = ['cochise11','cochise17','cochise19','cochise25']
    test_map['cochise19'] = ['cochise12','cochise18','cochise20','cochise26']
    test_map['cochise20'] = ['cochise13','cochise19','cochise21','cochise27']
    test_map['cochise21'] = ['cochise14','cochise20','cochise28']
    test_map['cochise22'] = ['cochise15','cochise23','cochise29']
    test_map['cochise23'] = ['cochise16','cochise22','cochise24','cochise30']
    test_map['cochise24'] = ['cochise17','cochise23','cochise25','cochise31']
    test_map['cochise25'] = ['cochise18','cochise24','cochise26','cochise32']
    test_map['cochise26'] = ['cochise19','cochise25','cochise27','cochise33']
    test_map['cochise27'] = ['cochise20','cochise26','cochise28','cochise34']
    test_map['cochise28'] = ['cochise21','cochise27','cochise35']
    test_map['cochise29'] = ['cochise22','cochise30','cochise36']
    test_map['cochise30'] = ['cochise23','cochise29','cochise31','cochise37']
    test_map['cochise31'] = ['cochise24','cochise30','cochise32','cochise38']
    test_map['cochise32'] = ['cochise25','cochise31','cochise33','cochise39']
    test_map['cochise33'] = ['cochise26','cochise32','cochise34','cochise40']
    test_map['cochise34'] = ['cochise27','cochise33','cochise35','cochise41']
    test_map['cochise35'] = ['cochise28','cochise34','cochise42']
    test_map['cochise36'] = ['cochise29','cochise37','cochise43']
    test_map['cochise37'] = ['cochise30','cochise36','cochise38','cochise44']
    test_map['cochise38'] = ['cochise31','cochise37','cochise39','cochise45']
    test_map['cochise39'] = ['cochise32','cochise38','cochise40','cochise46']
    test_map['cochise40'] = ['cochise33','cochise39','cochise41','cochise47']
    test_map['cochise41'] = ['cochise34','cochise40','cochise42','cochise48']
    test_map['cochise42'] = ['cochise35','cochise41','cochise49']
    test_map['cochise43'] = ['cochise36','cochise44']
    test_map['cochise44'] = ['cochise37','cochise43','cochise45']
    test_map['cochise45'] = ['cochise38','cochise44','cochise46']
    test_map['cochise46'] = ['cochise39','cochise45','cochise47']
    test_map['cochise47'] = ['cochise40','cochise46','cochise48']
    test_map['cochise48'] = ['cochise41','cochise47','cochise49']
    test_map['cochise49'] = ['cochise42','cochise48']

    #Coconino County
    test_map['coconino1'] = ['coconino', 'coconino', 'coconino2', 'coconino4']
    test_map['coconino2'] = ['coconino', 'coconino1', 'coconino3', 'coconino5']
    test_map['coconino3'] = ['coconino', 'coconino2', 'coconino', 'coconino6']
    test_map['coconino4'] = ['coconino1', 'coconino', 'coconino5', 'coconino7']
    test_map['coconino5'] = ['coconino2', 'coconino4', 'coconino6', 'coconino8']
    test_map['coconino6'] = ['coconino3', 'coconino5', 'coconino', 'coconino9']
    test_map['coconino7'] = ['coconino4', 'coconino', 'coconino8', 'coconino13']
    test_map['coconino8'] = ['coconino5', 'coconino7', 'coconino9', 'coconino14']
    test_map['coconino9'] = ['coconino6', 'coconino8', 'coconino10', 'coconino15']
    test_map['coconino10'] = ['coconino', 'coconino9', 'coconino11', 'coconino16']
    test_map['coconino11'] = ['coconino', 'coconino10', 'coconino12', 'coconino17']
    test_map['coconino12'] = ['coconino', 'coconino11', 'coconino', 'coconino18']
    test_map['coconino13'] = ['coconino7', 'coconino', 'coconino14', 'coconino21']
    test_map['coconino14'] = ['coconino8', 'coconino13', 'coconino15', 'coconino22']
    test_map['coconino15'] = ['coconino9', 'coconino14', 'coconino16', 'coconino23']
    test_map['coconino16'] = ['coconino10', 'coconino15', 'coconino17', 'coconino24']
    test_map['coconino17'] = ['coconino11', 'coconino16', 'coconino18', 'coconino25']
    test_map['coconino18'] = ['coconino12', 'coconino17', 'coconino19', 'coconino26']
    test_map['coconino19'] = ['coconino', 'coconino18', 'coconino20', 'coconino27']
    test_map['coconino20'] = ['coconino', 'coconino19', 'coconino', 'coconino28']
    test_map['coconino21'] = ['coconino13', 'coconino', 'coconino22', 'coconino29']
    test_map['coconino22'] = ['coconino14', 'coconino21', 'coconino23', 'coconino30']
    test_map['coconino23'] = ['coconino15', 'coconino22', 'coconino24', 'coconino31']
    test_map['coconino24'] = ['coconino16', 'coconino23', 'coconino25', 'coconino32']
    test_map['coconino25'] = ['coconino17', 'coconino24', 'coconino26', 'coconino33']
    test_map['coconino26'] = ['coconino18', 'coconino25', 'coconino27', 'coconino34']
    test_map['coconino27'] = ['coconino19', 'coconino26', 'coconino28', 'coconino35']
    test_map['coconino28'] = ['coconino20', 'coconino27', 'coconino', 'coconino36']
    test_map['coconino29'] = ['coconino21', 'coconino', 'coconino30', 'coconino37']
    test_map['coconino30'] = ['coconino22', 'coconino29', 'coconino31', 'coconino38']
    test_map['coconino31'] = ['coconino23', 'coconino30', 'coconino32', 'coconino39']
    test_map['coconino32'] = ['coconino24', 'coconino31', 'coconino33', 'coconino40']
    test_map['coconino33'] = ['coconino25', 'coconino32', 'coconino34', 'coconino41']
    test_map['coconino34'] = ['coconino26', 'coconino33', 'coconino35', 'coconino42']
    test_map['coconino35'] = ['coconino27', 'coconino34', 'coconino36', 'coconino43']
    test_map['coconino36'] = ['coconino28', 'coconino35', 'coconino', 'coconino44']
    test_map['coconino37'] = ['coconino29', 'coconino', 'coconino38', 'coconino45']
    test_map['coconino38'] = ['coconino30', 'coconino37', 'coconino39', 'coconino46']
    test_map['coconino39'] = ['coconino31', 'coconino38', 'coconino40', 'coconino47']
    test_map['coconino40'] = ['coconino32', 'coconino39', 'coconino41', 'coconino48']
    test_map['coconino41'] = ['coconino33', 'coconino40', 'coconino42', 'coconino49']
    test_map['coconino42'] = ['coconino34', 'coconino41', 'coconino43', 'coconino50']
    test_map['coconino43'] = ['coconino35', 'coconino42', 'coconino44', 'coconino51']
    test_map['coconino44'] = ['coconino36', 'coconino43', 'coconino', 'coconino52']
    test_map['coconino45'] = ['coconino37', 'coconino', 'coconino46', 'coconino53']
    test_map['coconino46'] = ['coconino38', 'coconino45', 'coconino47', 'coconino54']
    test_map['coconino47'] = ['coconino39', 'coconino46', 'coconino48', 'coconino55']
    test_map['coconino48'] = ['coconino40', 'coconino47', 'coconino49', 'coconino56']
    test_map['coconino49'] = ['coconino41', 'coconino48', 'coconino50', 'coconino57']
    test_map['coconino50'] = ['coconino42', 'coconino49', 'coconino51', 'coconino58']
    test_map['coconino51'] = ['coconino43', 'coconino50', 'coconino52', 'coconino59']
    test_map['coconino52'] = ['coconino44', 'coconino51', 'coconino', 'coconino60']
    test_map['coconino53'] = ['coconino45', 'coconino', 'coconino54', 'coconino61']
    test_map['coconino54'] = ['coconino46', 'coconino53', 'coconino55', 'coconino62']
    test_map['coconino55'] = ['coconino47', 'coconino54', 'coconino56', 'coconino63']
    test_map['coconino56'] = ['coconino48', 'coconino55', 'coconino57', 'coconino64']
    test_map['coconino57'] = ['coconino49', 'coconino56', 'coconino58', 'coconino65']
    test_map['coconino58'] = ['coconino50', 'coconino57', 'coconino59', 'coconino66']
    test_map['coconino59'] = ['coconino51', 'coconino58', 'coconino60', 'coconino67']
    test_map['coconino60'] = ['coconino52', 'coconino59', 'coconino', 'coconino']
    test_map['coconino61'] = ['coconino53', 'coconino', 'coconino62', 'coconino68']
    test_map['coconino62'] = ['coconino54', 'coconino61', 'coconino63', 'coconino69']
    test_map['coconino63'] = ['coconino55', 'coconino62', 'coconino64', 'coconino70']
    test_map['coconino64'] = ['coconino56', 'coconino63', 'coconino65', 'coconino71']
    test_map['coconino65'] = ['coconino57', 'coconino64', 'coconino66', 'coconino72']
    test_map['coconino66'] = ['coconino58', 'coconino65', 'coconino67', 'coconino73']
    test_map['coconino67'] = ['coconino59', 'coconino66', 'coconino', 'coconino74']
    test_map['coconino68'] = ['coconino61', 'coconino', 'coconino69', 'coconino']
    test_map['coconino69'] = ['coconino62', 'coconino68', 'coconino70', 'coconino']
    test_map['coconino70'] = ['coconino63', 'coconino69', 'coconino71', 'coconino']
    test_map['coconino71'] = ['coconino64', 'coconino70', 'coconino72', 'coconino']
    test_map['coconino72'] = ['coconino65', 'coconino71', 'coconino73', 'coconino']
    test_map['coconino73'] = ['coconino66', 'coconino72', 'coconino74', 'coconino']
    test_map['coconino74'] = ['coconino67', 'coconino73', 'coconino', 'coconino']

    #Gila County

    #Graham County

    #Greenlee County

    #La Paz County

    #Maricopa County

    #Mohave County

    #Navajo County

    #Pima County

    #Pinal County

    #Santa Cruz County

    #Yavapai County

    #Yuma County

    return test_map