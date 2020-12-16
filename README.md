# Globomap Metal to VM
Find which virtual machine are inside a physical server. Based on the "comp_unit" collection bellow:

    # comp_unit
    {
        id: <string>,
        name: <string>,
        provider: <string>,
        timestamp: <date>,
        properties: <object> {
            uuid: <string>,
            ...
            equipment_type: <string>,
            ips: <list> [<string>]
        }
    }


## ArangoDB Queries

    # query_physical_servers
    {
        "_key": "query_physical_servers",
        "name": "physical_servers",
        "description": "Servidores Físicos",
        "query": "FOR doc in @comp_unit FILTER LOWER(doc.properties.equipment_type) == LOWER('Servidor') FILTER CONTAINS(LOWER(doc.name), LOWER(@variable)) return doc",
        "params": {
            "@@comp_unit": "comp_unit"
        },
        "collection": ""
    }

    # query_physical_servers_by_ip
    {
        "_key": "query_physical_servers_by_ip",
        "name": "physical_servers_by_ip",
        "description": "Servidores Físicos por IP",
        "query": "FOR doc IN @@comp_unit FILTER LOWER(doc.properties.equipment_type) == LOWER('Servidor') FOR ip IN doc.properties.ips FILTER CONTAINS(ip, @variable) RETURN doc",
        "params": {
            "@@comp_unit": "comp_unit"
        },
        "collection": ""
    }
