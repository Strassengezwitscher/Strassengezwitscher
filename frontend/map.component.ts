import { Component, ViewChild, AfterViewInit } from "@angular/core";

import { MapObject } from "./mapObject";
import { MapObjectType } from "./map.service";
import { MapService } from "./map.service";

export class MapObjectSetting {
        constructor(public active: boolean = false, public iconPath: string, public name: string) {}
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
    // Utilized for holding status and name of different types of MapObjects
    private mapObjectSettings: Array<MapObjectSetting> = new Array<MapObjectSetting>();
    // Value list of different MapObject types to decrease redundant code
    private mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
    private markers: Map<MapObjectType, Array<google.maps.Marker>> = new Map<MapObjectType, Array<google.maps.Marker>>();

    @ViewChild("mapCanvas") private mapCanvas;

    constructor(private mapService: MapService) {
        this.initializeMarkerMap();
        this.initializeMapObjectSettings();
    }

    public ngAfterViewInit() {
        this.initMap();
        this.retrieveActiveMapObjects();
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

    private retrieveActiveMapObjects() {
        for (let mapObjectType of this.mapObjectTypes) {
            if (this.mapObjectSettings[mapObjectType].active) {
                this.mapService.getMapObjects(mapObjectType)
                            .subscribe(
                                mapObjects => this.drawMapObjects(mapObjects, mapObjectType),
                                error => this.errorMessage = <any>error
                            );
            }
        }
    }

    private drawMapObjects(mapObjects: MapObject[], mapObjectType: MapObjectType) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject, mapObjectType));
    }

    private drawMapObject(mapObject: MapObject, mapObjectType: MapObjectType) {
        const latLng = new google.maps.LatLng(mapObject.locationLat, mapObject.locationLong);
        const infoWindow = new google.maps.InfoWindow({
            content: mapObject.name,
        });
        const marker = new google.maps.Marker({
            position: latLng,
            title: mapObject.name,
            icon: this.mapObjectSettings[mapObjectType].iconPath
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

    private initializeMapObjectSettings() {
        this.mapObjectSettings[MapObjectType.EVENTS] = new MapObjectSetting(true, "static/img/schild_schwarz.png", "Veranstaltungen");
        this.mapObjectSettings[MapObjectType.FACEBOOK_PAGES] = new MapObjectSetting(false, "static/img/schild_blau.png", "Facebook-Seiten");
    }

    private initializeMarkerMap() {
        for (let mapObjectType of this.mapObjectTypes) {
            this.markers.set(mapObjectType, new Array<google.maps.Marker>());
        }
    }

    private deleteInactiveMapObjects() {
        for (let mapObjectType of this.mapObjectTypes) {
            if (!this.mapObjectSettings[mapObjectType].active && this.markers.get(mapObjectType).length > 0) {
                for (let marker of this.markers.get(mapObjectType)) {
                    marker.setMap(null);
                }
                this.markers.set(mapObjectType, new Array<google.maps.Marker>());
            }
        }
    }

    public onCheckboxChange() {
        this.retrieveActiveMapObjects();
        this.deleteInactiveMapObjects();
    }

    private showInfoWindowForMarker(marker: google.maps.Marker, infoWindow: google.maps.InfoWindow) {
        infoWindow.open(this.map, marker);
        this.currentlyOpenInfoWindow = infoWindow;
    }
}
