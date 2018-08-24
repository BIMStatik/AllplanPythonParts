<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ankotech_bolt.py</Name>
        <Title>ankotech_bolt</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>ankotech_bolt</Text>

       <Parameter>
            <Name>DiameterAnchorChar</Name>
            <Text>Durchmesser Anker</Text>
            <Value>C</Value>
            <ValueList>X|A|B|C|G|J|O|P|T|U</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>CountAnchor</Name>
            <Text>Anzahl Anker je Dübelleiste</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>Height</Name>
            <Text>Höhe</Text>
            <Value>150.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Length</Name>
            <Text>Länge</Text>
            <Value>450.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
       <Parameter>
            <Name>ColumnHeadCrossSection</Name>
            <Text>Querschnitt Stützenkopf</Text>
            <Value>Rechteck</Value>
            <!--<ValueList>Rechteck|Rund|Oval</ValueList>-->
            <ValueList>Linie|Rechteck|Rund</ValueList>-->
            <ValueType>StringComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>ColumnWidth</Name>
            <Text>x bei Linie, Breite bei Rechteck, Durchmesser bei Rund</Text>
            <Value>250</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>ColumnLength</Name>
            <Text>y bei Linie, Höhe bei Rechteck, Ignoriert bei Rund</Text>
            <Value>250</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>CountPart</Name>
            <Text>Anzahl Dübelleisten</Text>
            <Value>6</Value>
            <ValueType>Integer</ValueType>
        </Parameter>

    </Page>
</Element>
