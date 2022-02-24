import QtQuick 2.15
import QtQml 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2
import QtQuick.Controls.Styles 1.4
import QtGraphicalEffects 1.0

Window {

    Component.onCompleted: {
        requestActivate()
    }
    color: "#3B4252"
    objectName: "main_window"
    flags: Qt.BypassWindowManagerHint
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    visible: true
    width: 800
    height: 200

    onActiveChanged: {
        console.log("ciao")
    }

    Rectangle {
        objectName: "main_container"
        anchors.centerIn: parent
        width:  Window.window.width - 40
        height:  Window.window.height - 40
        color: "transparent"

        ColumnLayout {

            objectName: "main_column"
            spacing:10
            anchors.fill: parent

            Row {

                height: 30
                width: parent.width

                Text {
                    verticalAlignment: TextInput.AlignVCenter
                    color: "#a9b7c6"
                    text: "command: "
                    height: parent.height
                }

                TextInput {
                    id: search_field
                    verticalAlignment: TextInput.AlignVCenter
                    height: parent.height
                    Layout.fillWidth: true
                    color: "#a9b7c6"
                    activeFocusOnPress: true
                    cursorVisible: true
                    onAccepted: {
                        text_controller.on_enter(text)
                    }
                    Keys.onTabPressed: {
                        text=list_view.currentItem.children[0].text
                    }
                    Keys.onDownPressed: {
                        list_view.incrementCurrentIndex()
                        text=list_view.currentItem.children[0].text
                    }
                    Keys.onUpPressed: {
                        list_view.decrementCurrentIndex()
                        text=list_view.currentItem.children[0].text
                    }
                    onTextEdited: {
                        text_controller.on_edit(text)
                    }
                    Component.onCompleted: {
                        forceActiveFocus()
                    }
                }
            }
            Rectangle {
                id: "spacer"
                height: 1
                Layout.fillWidth: true
                color: "#5e81ac"
                layer.enabled: true
                layer.effect: DropShadow {
                    transparentBorder: true
                    horizontalOffset: 1
                    verticalOffset: 1
                    color: "#99000000"
                }
            }
            ListView {
                id: list_view
                keyNavigationEnabled: true
                keyNavigationWraps: true
                Layout.fillHeight: true
                width: parent.width
                clip: true
                cacheBuffer: 10
                model: filter

                highlight: Rectangle {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 10
                    color: "#2E3440"
                }

                delegate: Component {
                    Rectangle {
                        width: 100
                        height: 20
                        color: "transparent"
                        Text {
                            id: text_field
                            anchors.verticalCenter: parent.verticalCenter
                            color: "#a9b7c6"
                            text: model.name
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                controller.on_click(model.command)
                            }
                        }
                    }
                }
            }
        }
    }
}
