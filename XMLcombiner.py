import xml.etree.ElementTree as ET

PARENT_1_FILE = "ScoreboardLive.xml"
PARENT_2_FILE = "dash.xml"
CHILD_FILE = "data.xml"


#append parent files to child file repeatedly
def xmlCombine():
    list1 = ['flag', 'review']
    list2 = ['Hscore', 'Vscore']
    while True:
        try:
            #read parent 1 file
            with open(PARENT_1_FILE, "r") as parent1:
                xml1 = parent1.read()
            
            #read parent 2 file
            with open(PARENT_2_FILE, "r") as parent2:
                xml2 = parent2.read()

            #parsse parent files
            root1 = ET.fromstring(xml1)
            root2 = ET.fromstring(xml2)

            #create root element for child
            childRoot = ET.Element("info")


            for element in list2:
                if element is not None:
                    childElement = root1.find(element)
                    childRoot.append(childElement)

            for element in list1:
                if element is not None:
                    childElement = root2.find(element)
                    childRoot.append(childElement)

            childTree = ET.ElementTree(childRoot)

            childTree.write(CHILD_FILE)

        except Exception as e:
            print(f"Error {e}")
            break

xmlCombine()