import xml.etree.ElementTree as ET

xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<nlmSearchResult>
  <list>
    <document>
      <content>
        <title>Malaria</title>
        <summary>Malaria is a serious disease caused by parasites spread by mosquitoes.</summary>
        <url>https://medlineplus.gov/malaria.html</url>
        <date>2023-12-01</date>
      </content>
    </document>
    <document>
      <content>
        <title>Malaria Symptoms</title>
        <summary>Malaria symptoms include fever, chills, and headache.</summary>
        <url>https://medlineplus.gov/malaria-symptoms.html</url>
        <date>2023-11-15</date>
      </content>
    </document>
  </list>
  <count>2</count>
</nlmSearchResult>"""

# Debug the XML parsing
root = ET.fromstring(xml_data)
print("Root tag:", root.tag)

documents = root.findall('.//document')
print("Found documents:", len(documents))

for i, doc in enumerate(documents):
    print(f"Document {i}:")
    content = doc.find('content')
    if content is not None:
        print("  Content found")
        title_elem = content.find('title')
        summary_elem = content.find('summary')
        print(f"  Title: {title_elem.text if title_elem is not None else 'None'}")
        print(f"  Summary: {summary_elem.text if summary_elem is not None else 'None'}")
    else:
        print("  No content found")