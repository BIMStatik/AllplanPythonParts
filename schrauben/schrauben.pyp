<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>schrauben.py</Name>
        <Title>schrauben</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>

    <Page>
        <Name>SBS</Name>
        <Text>SBS</Text>
        
       <Parameter>
            <Name>sbs_screw</Name>
            <Text>Bolt Diameter</Text>
            <Value>M16</Value>
            <ValueList>M5|M6|M8|M10|M12|M16|M20|M24|M27|M30</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>sbs_color</Name>
            <Text>Farbe</Text>
            <Value>4</Value>
            <ValueType>Color</ValueType>
        </Parameter>
        <Parameter>
            <Name>sbs_length</Name>
            <Text>Laenge</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
    </Page>

    <Page>
        <Name>SHV</Name>
        <Text>SHV</Text>

        <Parameter>
            <Name>Color5</Name>
            <Text>Color</Text>
            <Value>5</Value>
            <ValueType>Color</ValueType>
        </Parameter>
        <Parameter>
            <Name>Length5</Name>
            <Text>Length</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Width5</Name>
            <Text>Width</Text>
            <Value>500.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Thickness5</Name>
            <Text>Thickness</Text>
            <Value>5000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
    </Page>
</Element>
