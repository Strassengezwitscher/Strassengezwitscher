import { Component, ViewChild, AfterViewInit } from "@angular/core";

import { MapObject } from "./mapObject";
import { MapObjectType } from "./map.service";
import { MapService } from "./map.service";

@Component({
    selector: "map-app",
    templateUrl: "map.component.html",
    providers: [MapService]
})

export class MapComponent implements AfterViewInit {

    currentlyOpenInfoWindow: google.maps.InfoWindow;
    errorMessage: string;
    map: google.maps.Map;
    showEvents: boolean = true;
    showPages: boolean = false;
    
    @ViewChild("mapCanvas") mapCanvas;

    constructor(private mapService: MapService) {}

    ngAfterViewInit() {
        this.initMap();
        this.getMapObjects(MapObjectType.EVENTS);
    }

    initMap() {
        const latlng = new google.maps.LatLng(51.0679567, 13.5767141);
        const mapOptions = {
            center: latlng,
            scrollWheel: false,
            zoom: 10
        };
        this.map = new google.maps.Map(this.mapCanvas.nativeElement, mapOptions);
    }

    getMapObjects(mapObjectType: MapObjectType) {
        this.mapService.getMapObjects(mapObjectType)
                        .subscribe(
                            mapObjects => this.drawMapObjects(mapObjects, mapObjectType),
                            error => this.errorMessage = <any>error
                        );
    }

    drawMapObjects(mapObjects: MapObject[], mapObjectType: MapObjectType) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject, mapObjectType));
    }

    drawMapObject(mapObject: MapObject, mapObjectType: MapObjectType) {
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

    onCheckboxChange(state: boolean) {
        console.log(state);
        console.log(this.showEvents);
        console.log(this.showPages);
    }

    showInfoWindowForMarker(marker: google.maps.Marker, infoWindow: google.maps.InfoWindow) {
        infoWindow.open(this.map, marker);
        this.currentlyOpenInfoWindow = infoWindow;
    }
}
