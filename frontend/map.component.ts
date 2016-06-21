import { Component, OnInit } from "@angular/core";

import { MapService } from "./map.service";
import { MapObject } from "./mapObject";

@Component({
    selector: "map-app",
    templateUrl: "map.component.html",
    providers: [MapService]
})
export class MapComponent implements OnInit {
    errorMessage: string;
    map: google.maps.Map;
    currentlyOpenInfoWindow: google.maps.InfoWindow;
    mode = 'Observable';

    constructor(private mapService: MapService) {}

    ngOnInit() {
        this.initMap();
        this.getMapObjects();
    }

    initMap() {
        const latlng = new google.maps.LatLng(52.3731, 4.8922);
        const mapOptions = {
            center: latlng,
            scrollWheel: false,
            zoom: 13
        };
        this.map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    }

    getMapObjects() {
        this.mapService.getMapObjects()
                        .subscribe(
                            mapObjects => this.drawMapObjects(mapObjects),
                            error => this.errorMessage = <any>error
                        );
    }

    drawMapObjects(mapObjects: MapObject[]) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject));
    }

    drawMapObject(mapObject: MapObject) {
        const latLng = new google.maps.LatLng(mapObject.location_lat, mapObject.location_long);
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

    closeCurrentlyOpenInfoWindow() {
        if (this.currentlyOpenInfoWindow) {
            this.currentlyOpenInfoWindow.close();
        }
    }

    showInfoWindowForMarker(marker: google.maps.Marker, infoWindow: google.maps.InfoWindow) {
        infoWindow.open(this.map, marker);
        this.currentlyOpenInfoWindow = infoWindow;
    }
}
