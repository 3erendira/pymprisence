from jeepney import DBusAddress, new_method_call
from jeepney.io.blocking import open_dbus_connection

class MPRIS:
    def __init__(self):
        self.conn = open_dbus_connection(bus="SESSION")

    def getAddress(self, player) -> DBusAddress:
        address = DBusAddress('/org/mpris/MediaPlayer2',
                              bus_name=player,
                              interface="org.mpris.MediaPlayer2.Player")
        return address
    
    def getPlayers(self) -> list[str]:
        address = DBusAddress("/org/freedesktop/DBus",
                              bus_name="org.freedesktop.DBus",
                              interface="org.freedesktop.DBus")
        players = []

        msg = new_method_call(address, "ListNames")
        reply = self.conn.send_and_get_reply(msg)
        for iface in reply.body[0]:
            if iface.startswith("org.mpris.MediaPlayer2."):
                players.append(iface)

        return players

    def getMetadata(self) -> dict:
        obj = self.getAddress("org.mpris.MediaPlayer2.fooyin")
        props_if = DBusAddress(obj.object_path,
                              bus_name=obj.bus_name,
                              interface="org.freedesktop.DBus.Properties")
        msg = new_method_call(props_if,
                                "Get",
                                "ss",
                                (obj.interface, "Metadata"))
        reply = self.conn.send_and_get_reply(msg)
        return reply.body[0][1]
    
    def getPosition(self) -> int:
        obj = self.getAddress("org.mpris.MediaPlayer2.fooyin")
        props_if = DBusAddress(obj.object_path,
                              bus_name=obj.bus_name,
                              interface="org.freedesktop.DBus.Properties")
        msg = new_method_call(props_if,
                                "Get",
                                "ss",
                                (obj.interface, "Position"))
        reply = self.conn.send_and_get_reply(msg)
        return reply.body[0][1]
    
    def getPlaybackStatus(self) -> bool | str:
        obj = self.getAddress("org.mpris.MediaPlayer2.fooyin")
        props_if = DBusAddress(obj.object_path,
                              bus_name=obj.bus_name,
                              interface="org.freedesktop.DBus.Properties")
        msg = new_method_call(props_if,
                                "Get",
                                "ss",
                                (obj.interface, "PlaybackStatus"))
        reply = self.conn.send_and_get_reply(msg)
        if reply == "Playing":
            return True
        elif reply == "Paused" or "Stopped":
            return False
        
        return reply.body[0][1]