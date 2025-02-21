import QtQuick 2.15
import QtQuick.Controls 2.15
import QtLocation 5.15
import QtPositioning 5.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "QtLocation Map Example"

    Map {
        id: map
        anchors.fill: parent
        plugin: Plugin {
            name: "osm"
            PluginParameter {
                name: "osm.mapping.tileserver.base_url"
                value: "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            }
        }
        center: mapUpdater.centerCoordinate
        zoomLevel: 12

        MapPolyline {
            id: routeline
            width: 4
            path: mapUpdater.pathCoordinates
        }
    }
}
