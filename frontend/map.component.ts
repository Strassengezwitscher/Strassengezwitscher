import { Component, OnInit } from "@angular/core";

import { MapService } from "./map.service";
import { MapObject } from "./mapObject";

@Component({
    selector: "map-app",
    templateUrl: "map.component.html",
    providers: [MapService]
})
export class MapComponent implements OnInit {

    map: google.maps.Map;
    currentlyOpenInfoWindow: google.maps.InfoWindow;

    constructor(private mapService: MapService) {}

    closeCurrentlyOpenInfoWindow() {
        if (this.currentlyOpenInfoWindow) {
            this.currentlyOpenInfoWindow.close();
        }
    }

    drawMapObject(mapObject: MapObject) {
        const latLng = new google.maps.LatLng(mapObject.locationLat, mapObject.locationLong);
        const infoWindow = new google.maps.InfoWindow({
            content: mapObject.name
        });
        const marker = new google.maps.Marker({
            position: latLng,
            title: mapObject.name
        });

        marker.addListener("click", (() => {
            this.closeCurrentlyOpenInfoWindow();
            this.showInfoWindowForMarker(marker, infoWindow);
        }));
        marker.setMap(this.map);
    }

    drawMapObjects(mapObjects: MapObject[]) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject));
    }

    getMapObjects() {
        this.mapService.getMapObjects().then(mapObjects => this.drawMapObjects(mapObjects));
    }

    ngOnInit() {
        const latlng = new google.maps.LatLng(52.3731, 4.8922);
        const mapOptions = {
          center: latlng,
          scrollWheel: false,
          zoom: 13
        };
        this.map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

        this.getMapObjects();
    }

    showInfoWindowForMarker(marker: google.maps.Marker, infoWindow: google.maps.InfoWindow) {
        infoWindow.open(this.map, marker);
        this.currentlyOpenInfoWindow = infoWindow;
    }
}
