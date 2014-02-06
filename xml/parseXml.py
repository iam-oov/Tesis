import xml.etree.ElementTree as ET

def prettify(elem):
	from xml.etree import ElementTree
	from xml.dom import minidom
	"""Return a pretty-printed XML string for the Element.
	"""
	# rough_string = ElementTree.tostring(elem, 'utf-8')
	# reparsed = minidom.parseString(rough_string)
	return elem.toprettyxml(indent="  ")



tree = ET.parse('colonias.xml')
root = tree.getroot()

for child in root:
	print child.tag, child.attrib
print '...'

# encuentra todas la etiquetas con el mismo nombre
for colonia in root.iter('colonia'):
	print colonia.attrib
print 'xxx'

for municipios in root.findall('municipio'):
	municipio = municipios.get('nombre')
	alcalde = municipios.find('alcalde').text
	print municipio, alcalde

# modificar
for fund in root.iter('fundacion'):
	new_rank = int(fund.text) + 1
	fund.text = str(new_rank)
	fund.set('updated', 'yes') # para agregar un nuevo atributo
tree.write('output.xml')

# eliminar elementos
for minicipios in root.findall('municipio'):
	ano = int(minicipios.find('fundacion').text)
	if ano > 50:
		root.remove(minicipios)


# from xml.etree.ElementTree import Element, SubElement, Comment

# top = Element('top')

# comment = Comment('Generated for PyMOTW')
# top.append(comment)

# child = SubElement(top, 'child')
# child.text = 'This child contains text.'

# child_with_tail = SubElement(top, 'child_with_tail')
# child_with_tail.text = 'This child has regular text.'
# child_with_tail.tail = 'And "tail" text.'

# child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
# child_with_entity_ref.text = 'This & that'
# print prettify(top)


root = ET.Element("root")

doc = ET.SubElement(root, "doc")

field1 = ET.SubElement(doc, "field1")
field1.set("name", "blah")
field1.text = "some value1"

field2 = ET.SubElement(doc, "field2")
field2.set("name", "asdfasd")
field2.text = "some vlaue2"

print prettify(root)
root2 = prettify(root)

tree = ET.ElementTree(root2)
tree.write("filename.xml")


