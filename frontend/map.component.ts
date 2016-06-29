import { Component, ViewChild, AfterViewInit } from "@angular/core";

import { MapService } from "./map.service";
import { MapObject } from "./mapObject";

@Component({
    selector: "sg-map",
    templateUrl: "map.component.html",
    providers: [MapService],
})
export class MapComponent implements AfterViewInit {
    private errorMessage: string;
    private map: google.maps.Map;
    private currentlyOpenInfoWindow: google.maps.InfoWindow;
    @ViewChild("mapCanvas") private mapCanvas;

    constructor(private mapService: MapService) {}

    public ngAfterViewInit() {
        this.initMap();
        this.getMapObjects();
    }

    private initMap() {
        const latlng = new google.maps.LatLng(52.3731, 4.8922);
        const mapOptions = {
            center: latlng,
            scrollWheel: false,
            zoom: 13,
        };
        this.map = new google.maps.Map(this.mapCanvas.nativeElement, mapOptions);
    }

    private getMapObjects() {
        this.mapService.getMapObjects()
                        .subscribe(
                            mapObjects => this.drawMapObjects(mapObjects),
                            error => this.errorMessage = <any> error,
                        );
    }

    private drawMapObjects(mapObjects: MapObject[]) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject));
    }

    private drawMapObject(mapObject: MapObject) {
        const latLng = new google.maps.LatLng(mapObject.location_lat, mapObject.location_long);
        const infoWindow = new google.maps.InfoWindow({
            content: mapObject.name,
        });
        const marker = new google.maps.Marker({
            position: latLng,
            title: mapObject.name,
        });

        marker.addListener("click", (() => {
            this.closeCurrentlyOpenInfoWindow();
            this.showInfoWindowForMarker(marker, infoWindow);
        }));
        marker.setMap(this.map);
    }

    private closeCurrentlyOpenInfoWindow() {
        if (this.currentlyOpenInfoWindow) {
            this.currentlyOpenInfoWindow.close();
        }
    }

    private showInfoWindowForMarker(marker: google.maps.Marker, infoWindow: google.maps.InfoWindow) {
        infoWindow.open(this.map, marker);
        this.currentlyOpenInfoWindow = infoWindow;
    }
}
