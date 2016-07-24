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

    private currentlyOpenInfoWindow: google.maps.InfoWindow;
    private errorMessage: string;
    private map: google.maps.Map;
    private markers: Map<MapObjectType, Array<google.maps.Marker>> = new Map<MapObjectType, Array<google.maps.Marker>>();
    private markerImageMap: Map<MapObjectType, string> = new Map<MapObjectType, string>();
    private showEvents: boolean = true;
    private showPages: boolean = false;
    
    @ViewChild("mapCanvas") mapCanvas;

    constructor(private mapService: MapService) {
        this.initializeMarkerImageMap();
        this.initializeMarkerMap();
    }

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
            title: mapObject.name,
            icon: this.markerImageMap.get(mapObjectType)
        });

        marker.addListener("click", (() => {
            this.closeCurrentlyOpenInfoWindow();
            this.showInfoWindowForMarker(marker, infoWindow);
        }));
        marker.setMap(this.map);
        this.markers.get(mapObjectType).push(marker);
    }

    closeCurrentlyOpenInfoWindow() {
        if (this.currentlyOpenInfoWindow) {
            this.currentlyOpenInfoWindow.close();
        }
    }

    initializeMarkerImageMap() {
        this.markerImageMap.set(MapObjectType.EVENTS, "static/img/schild_schwarz.png");
        this.markerImageMap.set(MapObjectType.FACEBOOK_PAGES, "static/img/schild_blau.png");
    }

    initializeMarkerMap() {
        const mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
        for (let mapObjectType of mapObjectTypes) {
            this.markers.set(mapObjectType, new Array<google.maps.Marker>());
        }
    }

    deleteMarkers(mapObjectType: MapObjectType) {
        for (let marker of this.markers.get(mapObjectType)) {
            marker.setMap(null);
        }
        this.markers.set(mapObjectType, new Array<google.maps.Marker>());
    }

    onEventCheckboxChange() {
        let mapObjectType: MapObjectType = MapObjectType.EVENTS;
        console.log(mapObjectType);
        if (this.showEvents) {
            this.getMapObjects(mapObjectType);
        } else {
            this.deleteMarkers(mapObjectType);
        }
    }

    onFacebookCheckboxChange() {
        let mapObjectType: MapObjectType = MapObjectType.FACEBOOK_PAGES;
        if (this.showEvents) {
            this.getMapObjects(mapObjectType);
        } else {
            this.deleteMarkers(mapObjectType);
        }
    }

    showInfoWindowForMarker(marker: google.maps.Marker, infoWindow: google.maps.InfoWindow) {
        infoWindow.open(this.map, marker);
        this.currentlyOpenInfoWindow = infoWindow;
    }
}
