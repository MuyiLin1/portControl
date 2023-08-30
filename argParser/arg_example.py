import argparse

PORT_ON = 1
PORT_OFF = 0
PORT_STATUS = 2
#can be changed to max string length if ports come longer than 20 characters
width = 20

# Map for all connections/ports connected to Sonatus Breakout Board, and the actual relay that does it.
relay2port = {
    "SNPWR_1": "CCU",
    "SNPWR_2": "MEDIA_GATEWAY",
    "SNPWR_3": "MEDIA_CONVERTER_4x",
    "SNPWR_4": "PEAK_OR_CANCOMBO",
    "SNPWR_5": "",
    "SNPWR_6": "",
    "SNPWR_7": "",
    "SNPWR_8": "ALL_USB_HUB",
    "WAKES_1": "",
    "WAKES_2": "L_WK_CCIC",
    "WAKES_3": "L_WK_DCU",
    "WAKES_4": "L_WK_DVRS",
    "WAKES_5": "",
    "WAKES_6": "",
    "WAKES_7": "",
    "WAKES_8": "",
    "GPIOS_1": "IGN1",
    "GPIOS_2": "ACC",
    "GPIOS_3": "IGN3",
    "GPIOS_4": "ERT_ACT",
    "GPIOS_5": "",
    "GPIOS_6": "",
    "GPIOS_7": "",
    "GPIOS_8": "",
    "COPEN_1": "DVRS",
    "COPEN_2": "HDM",
    "COPEN_3": "ADASPRK",
    "COPEN_4": "CCIC",
    "COPEN_5": "",
    "COPEN_6": "",
    "COPEN_7": "",
    "COPEN_8": "",
    "SHORT_1": "CLU",
    "SHORT_2": "ADAS_DRV",
    "SHORT_3": "ADAS_VP",
    "SHORT_4": "DCU",
    "SHORT_5": "",
    "SHORT_6": "",
    "SHORT_7": "",
    "ERTSW_1": "",
    "ERTSW_2": "",
    "ERTSW_3": "",
    "ERTSW_4": "",
    "CCUBT_1": "",
    "CCUBT_2": "",
}

def usbrelay_cmd():
    return '''SNPWR_1=1
        SNPWR_2=1
        SNPWR_3=1
        SNPWR_4=1
        SNPWR_5=1
        SNPWR_6=1
        SNPWR_7=1
        SNPWR_8=1
        GPIOS_1=1
        GPIOS_2=1
        GPIOS_3=1
        GPIOS_4=1
        GPIOS_5=1
        GPIOS_6=1
        GPIOS_7=1
        GPIOS_8=1
        WAKES_1=1
        WAKES_2=1
        WAKES_3=1
        WAKES_4=1
        WAKES_5=1
        WAKES_6=1
        WAKES_7=1
        WAKES_8=1
        CCUBT_1=0
        CCUBT_2=0'''


def swap_dict(d):
    swapped_d = {}
    for k, v in d.items():
        if v != "" and v is not None:
            swapped_d[v] = k
    return swapped_d


def print_dict(d):
    for k, v in d.items():
        print(f'"{k}": "{v}"')
        
def split_current_status():
    output = usbrelay_cmd()
    outputList = output.split("\n")
    lst = []
    for item in outputList:
        lst.append(item.strip().split("="))
    return lst
    

port2relay = swap_dict(relay2port)
port2relayKeys = list(port2relay.keys())
port2relayKeys.append("all")

#made so that if it isnt correct port or state then it produces an error
def main():
    
    parser = argparse.ArgumentParser(description="User end script for control all ports on the Breakout Board")

    # Positional argument
    parser.add_argument("port", help="Specific port", choices=port2relayKeys)
    
    #CHANGE NAME STATUS TO WHATEVER SEEMS FIT
    parser.add_argument("action", help="State of being on or off or getting the status", choices=["on","off","status"])
    args = parser.parse_args()
    
    #default is status
    value = PORT_STATUS
    if args.action.lower() == "on":
        value = PORT_ON
    elif args.action.lower() == "off":
        value = PORT_OFF
    
        
    #BIG ISSUE, WHEN I CALL ALL OFF IT PRINTS IT OUT WITH ALL OF THEM AT VALUE 0
    #WHEN I CALL A SPECIFIC PORT ON OR OFF THE REST OF THEM GO BACK TO THE OLD VALUES
    
    #my all on/off is not changing the dictionary values
    if args.port == "all":
        if value == PORT_STATUS:
            outputList = split_current_status()
            for item in outputList:
                port, status = item
                #skip if relay2port value is empty
                if relay2port[port] == "":
                    continue
                print(f"{relay2port[port] : <{width}} {'on' if status == '1' else 'off'}")
                
        #if you want you can make a list of ports you want to turn on
        # else:
        #     for port in port2relayKeys:
        #         print(port)
        #         if port == "all":
        #             continue
        #         port2relay[f"{port}"] = value
        #         print(port2relay[port])
        #     print(f"All ports turned {args.action}")
        
    else:
        if value == PORT_STATUS:
            outputList = split_current_status()
            for item in outputList:
                relay_port, status = item
                if relay2port[relay_port] == args.port:
                    print(f"{args.port} \t{'on' if status == '1' else 'off'}")
        else:
            relay_port = port2relay[f"{args.port}"]
            value = args.action
            print(f" {args.port} turned {args.action}")
            cmd = f"usbrelay {relay_port}={'1' if value == 'on' else '0'}"
            print(f'Running this cmd: {cmd}')
            #Check relay port setting
        
            output = usbrelay_cmd()



if __name__ == "__main__":
    main()
