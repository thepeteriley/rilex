// Original Rilex installation slide. SPDX-License-Identifier: MIT
import QtQuick 2.0
import calamares.slideshow 1.0

Presentation {
    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#20252c"
            Text {
                anchors.centerIn: parent
                width: parent.width * 0.8
                color: "#e3e7ed"
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 22
                text: qsTr("Rilex: a desktop built for keyboards.\n\nSuper+Enter opens a terminal.\nSuper+Space launches applications.\nSuper+/ opens the shortcut reference.\n\nPlease wait while installation finishes.")
            }
        }
    }
}
