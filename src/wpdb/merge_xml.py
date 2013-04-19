"""
A general purpose utility for merging XML files. Ignorant of XML schema and namespaces.
 
Author: Paul Barton - SavinaRoja
"""
 
import xml.dom.minidom as minidom
from hashlib import sha1
 
def element_hash(self):
    """
    Provides a means of hashing an element. This method only accounts for
    tag names and attribute-value pairs.
 
    It composes a string of the tag name, followed by alphabetized (by
    attribute name) attribute-value pairs. It then converts this to an integer
    for hash comparison.
    """
    hash_string = self.tagName
    attribute_keys = sorted(self.attributes.keys())
    for attr_key in attribute_keys:
        hash_string += '{0}{1}'.format(attr_key, self.attributes[attr_key].value)
    return int(sha1(hash_string).hexdigest(), 16)
 
def text_hash(self):
    """
    Provides a means of hashing a Text node. It just hashes the text data.
    """
    hash_string = self.data
    return int(sha1(hash_string).hexdigest(), 16)
 
def element_equals(self, other):
    """
    Boolean comparison of Elements. Compares the integers from Element.__hash__
    which is also patched into the class. See element_hash.
    """
    if self.__hash__() == other.__hash__():
        return True
    else:
        return False
 
def element_hash_children(self):
    """
    Creates a dictionary of child elements; the element serving as value and
    the hash serving as the key.
    """
    child_dict = {}
    for child in self.childNodes:
        child_dict[hash(child)] = child
    return child_dict
 
#Monkey patching some methods into xml.dom.minidom Classes
minidom.Element.__hash__ = element_hash
minidom.Element.__eq__ = element_equals
minidom.Element.hashedChildNodes = element_hash_children
minidom.Text.__hash__ = text_hash
minidom.Text.hashedChildNodes = {}
 
def xml_merge(reference_element, subject_element):
    """
    Recursively traverses a subject XML tree and a reference tree, merging the
    subject tree Elements into the reference tree if the subject Element is
    unique.
    """
    for subject_child in subject_element.childNodes:
        subject_hash = hash(subject_child)
        if subject_hash in reference_element.hashedChildNodes():
            reference_child = reference_element.hashedChildNodes()[subject_hash]
            xml_merge(reference_child, subject_child)
        else:
            reference_element.appendChild(subject_child)
    return