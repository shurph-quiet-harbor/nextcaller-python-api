import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from pynextcaller.tests.base import BaseTestCase


PHONE_JSON_RESULT_EXAMPLE = '''
{
    "records": [
        {
            "id": "97d949a413f4ea8b85e9586e1f2d9a",
            "first_name": "Jerry",
            "last_name": "Seinfeld",
            "name": "Jerry Seinfeld",
            "language": "English",
            "fraud_threat": "low",
            "spoof": "false",
            "phone": [
                {
                    "number": "2125558383"
                }
            ],
            "carrier": "Verizon Wireless",
            "line_type": "LAN",
            "address": [
                {
                    "city": "New York",
                    "extended_zip": "",
                    "country": "USA",
                    "line2": "Apt 5a",
                    "line1": "129 West 81st Street",
                    "state": "NY",
                    "zip_code": "10024"
                }
            ],
            "email": "demo@nextcaller.com",
            "age": "45-54",
            "gender": "Male",
            "household_income": "50k-75k",
            "marital_status": "Single",
            "presence_of_children": "No",
            "home_owner_status": "Rent",
            "market_value": "350k-500k",
            "length_of_residence": "12 Years",
            "high_net_worth": "No",
            "occupation": "Entertainer",
            "education": "Completed College",
            "department": "not specified"
        }
    ]
}
'''

PHONE_XML_RESULT_EXAMPLE = '''
<response>
    <records>
        <object>
            <id>97d949a413f4ea8b85e9586e1f2d9a</id>
            <first_name>Jerry</first_name>
            <last_name>Seinfeld</last_name>
            <name>Jerry Seinfeld</name>
            <language>English</language>
            <fraud_threat>low</fraud_threat>
            <spoof>false</spoof>
            <phone>
                <object>
                    <number>2125558383</number>
                </object>
            </phone>
            <carrier>Verizon Wireless</carrier>
            <line_type>LAN</line_type>
            <address>
                <object>
                    <line1>129 West 81st Street</line1>
                    <line2>Apt 5a</line2>
                    <city>New York</city>
                    <state>NY</state>
                    <zip_code>10024</zip_code>
                    <extended_zip/>
                    <country>USA</country>
                </object>
            </address>
            <email>demo@nextcaller.com</email>
            <age>45-54</age>
            <gender>Male</gender>
            <household_income>50k-75k</household_income>
            <marital_status>Single</marital_status>
            <presence_of_children>No</presence_of_children>
            <home_owner_status>Rent</home_owner_status>
            <market_value>350k-500k</market_value>
            <length_of_residence>12 Years</length_of_residence>
            <high_net_worth>No</high_net_worth>
            <occupation>Entertainer</occupation>
            <education>Completed College</education>
            <department>not specified</department>
        </object>
    </records>
</response>'''


class PhoneTestCase(BaseTestCase):

    def test_by_phone_json_request(self):
        phone = '2125558383'
        self.patch_http_request(PHONE_JSON_RESULT_EXAMPLE)
        res = self.client.get_by_phone(phone)
        self.assertTrue(res['records'])
        self.assertEqual(res['records'][0]['email'], 'demo@nextcaller.com')
        self.assertEqual(res['records'][0]['first_name'], 'Jerry')
        self.assertEqual(res['records'][0]['last_name'], 'Seinfeld')

    def test_phone_xml_request(self):
        phone = '2125558383'
        self.patch_http_request(PHONE_XML_RESULT_EXAMPLE)
        res = self.client.get_by_phone(phone, response_format='xml')
        record = res.getElementsByTagName('response')[0].\
            getElementsByTagName('records')[0]
        self.assertTrue(record)
        self.assertEqual(
            record.getElementsByTagName('email')[0].firstChild.nodeValue,
            'demo@nextcaller.com')
        self.assertEqual(
            record.getElementsByTagName('first_name')[0].firstChild.nodeValue,
            'Jerry')
        self.assertEqual(
            record.getElementsByTagName('last_name')[0].firstChild.nodeValue,
            'Seinfeld')

if __name__ == '__main__':
    unittest.main()
