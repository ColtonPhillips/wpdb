"""
A general purpose utility for merging XML files. Ignorant of XML schema and namespaces.
 
Written for use with Python2, using lxml
 
Author: Paul Barton - SavinaRoja
"""
 
import lxml.etree
from hashlib import sha1
 
def text_hash(text):
    """
    Hashes text, for self.text and self.tail.
    """
    hash_string = u'{0}'.format(text)
    return int(sha1(hash_string.encode('utf-8')).hexdigest(), 16)
 
def element_hash(element):
    """
    Provides a means of hashing an element. This method only accounts for
    tag names and attribute-value pairs.
 
    It composes a string of the tag name, followed by alphabetized (by
    attribute name) attribute-value pairs. It then converts this to an integer
    for hash comparison.
    """
    hash_string = u'{0}'.format(element.tag)
    attribute_keys = sorted(element.attrib.keys())
    for attr_key in attribute_keys:
        hash_string += u'{0}{1}'.format(attr_key, element.attrib[attr_key])
    return int(sha1(hash_string.encode('utf-8')).hexdigest(), 16)
 
def hashed_children(element):
    """
    Creates a dictionary of child elements; the element serving as value and
    the hash serving as the key.
    """
    child_dict = {}
    if element.text:
        child_dict[text_hash(element.text)] = element.text
    if element.tail:
        child_dict[text_hash(element.tail)] = element.tail
    for child in element.getchildren():
        child_dict[element_hash(child)] = child
    return child_dict
 
 
def get_list_with_text(element):
    try:
        return [element.text, element.tail] + list(element)
    except AttributeError:  # Receives a string
        return []
        
 
def xml_merge(reference_element, subject_element):
    """
    Recursively traverses a subject XML tree and a reference tree, merging the
    subject tree Elements into the reference tree if the subject Element is
    unique.
    """
    for subject_child in get_list_with_text(subject_element):
        #First get the relevant hash
        if isinstance(subject_child, lxml.etree._Element):  # Element
            text = False
            subject_hash = element_hash(subject_child)
        elif subject_child is None:  # An empty text or tail
            continue
        else:  # Nonempty text or tail
            text = True
            subject_hash = text_hash(subject_child)
 
        #Then look to see if it is already in the target's hashed children
        if subject_hash in hashed_children(reference_element):
            reference_child = hashed_children(reference_element)[subject_hash]
            xml_merge(reference_child, subject_child)
        #If it is not, append it
        else:
            if text:  #Append all text to the tail
                try:
                    reference_element.tail += subject_child
                except TypeError:  # Empty tail
                    reference_element.tail = subject_child
            else:  #Append all elements to the end of the children
                reference_element.append(subject_child)
    return