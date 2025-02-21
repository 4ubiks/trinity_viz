import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

Item {
    width: 400
    height: 400

    Rectangle {
        id: background
        anchors.fill: parent
        color: "#222222"
    }

    View3D {
        id: view
        anchors.fill: parent

        environment: SceneEnvironment {
            clearColor: "transparent"
            backgroundMode: SceneEnvironment.Transparent
        }

        PerspectiveCamera {
            id: camera
            position: Qt.vector3d(0, 0, 10)
            clipNear: 1.0
        }

        DirectionalLight {
            eulerRotation.x: -30
            eulerRotation.y: -70
            ambientColor: Qt.rgba(0.5, 0.5, 0.5, 1.0)
        }

        SaturnV {
            id: node
            position: Qt.vector3d(0, 0, 0)
            scale: Qt.vector3d(1, 1, 1)
            eulerRotation: Qt.vector3d(rotationHandler.rotationX, rotationHandler.rotationY, rotationHandler.rotationZ)
        }
    }
}
