from jeepney import DBusAddress, new_method_call
from jeepney.io.blocking import open_dbus_connection

class MPRIS:
    def __init__(self):
        self.conn = open_dbus_connection(bus="SESSION")

    def get_address(self, player) -> DBusAddress:
        address = DBusAddress('/org/mpris/MediaPlayer2',
                              bus_name=player,
                              interface="org.mpris.MediaPlayer2.Player")
        return address
    
    def get_players(self) -> list[str]:
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

    def get_metadata(self) -> dict:
        obj = self.get_address("org.mpris.MediaPlayer2.fooyin")
        props_if = DBusAddress(obj.object_path,
                              bus_name=obj.bus_name,
                              interface="org.freedesktop.DBus.Properties")
        msg = new_method_call(props_if,
                                "Get",
                                "ss",
                                (obj.interface, "Metadata"))
        reply = self.conn.send_and_get_reply(msg)
        return reply.body[0][1]
    
    def get_position(self) -> int:
        obj = self.get_address("org.mpris.MediaPlayer2.fooyin")
        props_if = DBusAddress(obj.object_path,
                              bus_name=obj.bus_name,
                              interface="org.freedesktop.DBus.Properties")
        msg = new_method_call(props_if,
                                "Get",
                                "ss",
                                (obj.interface, "Position"))
        reply = self.conn.send_and_get_reply(msg)
        return reply.body[0][1]
    
    def get_playback_status(self) -> bool | str:
        obj = self.get_address("org.mpris.MediaPlayer2.fooyin")
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