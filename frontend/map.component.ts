import { Component, ViewChild, AfterViewInit } from "@angular/core";

import { MapObject } from "./mapObject";
import { MapObjectType } from "./map.service";
import { MapService } from "./map.service";

export class MapObjectSetting {
        constructor(name: string, active: boolean = false) {
            this.name = name;
            this.active = active;
        }

    public name: string;
    public active: boolean = false;
}

@Component({
    selector: "sg-map",
    templateUrl: "map.component.html",
    providers: [MapService],
})

export class MapComponent implements AfterViewInit {

    private currentlyOpenInfoWindow: google.maps.InfoWindow;
    private errorMessage: string;
    private map: google.maps.Map;
    private mapObjectSettings: Array<MapObjectSetting> = new Array<MapObjectSetting>();
    private markers: Map<MapObjectType, Array<google.maps.Marker>> = new Map<MapObjectType, Array<google.maps.Marker>>();
    private markerImageMap: Map<MapObjectType, string> = new Map<MapObjectType, string>();
    
    @ViewChild("mapCanvas") private mapCanvas;

    constructor(private mapService: MapService) {
        this.initializeMarkerImageMap();
        this.initializeMarkerMap();
        this.mapObjectSettings[MapObjectType.EVENTS] = new MapObjectSetting("Veranstaltungen", true);
        this.mapObjectSettings[MapObjectType.FACEBOOK_PAGES] = new MapObjectSetting("Facebook-Seiten", false);
    }

    public ngAfterViewInit() {
        this.initMap();
        this.getActiveMapObjects();
    }

    private initMap() {
        const latlng = new google.maps.LatLng(51.0679567, 13.5767141);
        const mapOptions = {
            center: latlng,
            scrollWheel: false,
            zoom: 10
        };
        this.map = new google.maps.Map(this.mapCanvas.nativeElement, mapOptions);
    }

    getActiveMapObjects() {
        const mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
        for (let mapObjectType of mapObjectTypes) {
            if (this.mapObjectSettings[mapObjectType].active) {
                this.mapService.getMapObjects(mapObjectType)
                            .subscribe(
                                mapObjects => this.drawMapObjects(mapObjects, mapObjectType),
                                error => this.errorMessage = <any>error
                            );
            }
        }
    }

    drawMapObjects(mapObjects: MapObject[], mapObjectType: MapObjectType) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject, mapObjectType));
    }

    drawMapObject(mapObject: MapObject, mapObjectType: MapObjectType) {
        const latLng = new google.maps.LatLng(mapObject.locationLat, mapObject.locationLong);
        const infoWindow = new google.maps.InfoWindow({
            content: mapObject.name,
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

    private closeCurrentlyOpenInfoWindow() {
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

    deleteInactiveMapObjects() {
        const mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
        for (let mapObjectType of mapObjectTypes) {
            if (!this.mapObjectSettings[mapObjectType].active && this.markers.get(mapObjectType).length > 0) {
                for (let marker of this.markers.get(mapObjectType)) {
                    marker.setMap(null);
                }
                this.markers.set(mapObjectType, new Array<google.maps.Marker>());
            }
        }
    }

    onCheckboxChange() {
        this.getActiveMapObjects();
        this.deleteInactiveMapObjects();
    }

    private showInfoWindowForMarker(marker: google.maps.Marker, infoWindow: google.maps.InfoWindow) {
        infoWindow.open(this.map, marker);
        this.currentlyOpenInfoWindow = infoWindow;
    }
}
