import { Component, ViewChild, AfterViewInit, NgZone } from "@angular/core";

import { MapObject, MapObjectType, MapService } from "./";

class MapObjectSetting {
        constructor(public visible: boolean = false, public iconPath: string,
                    public iconClickedPath: string, public name: string) {}
}

@Component({
    moduleId: module.id,
    selector: "cg-map",
    templateUrl: "map.component.html",
    providers: [MapService],
})

export class MapComponent implements AfterViewInit {

    private errorMessage: string;
    private errorMessageDisplayTime: number = 5000;
    private map: google.maps.Map;
    // Utilized for holding status and name of different types of MapObjects
    private mapObjectSettings: Array<MapObjectSetting> = new Array<MapObjectSetting>();
    // Value list of different MapObject types to decrease redundant code
    private mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
    private markers: Map<MapObjectType, Array<google.maps.Marker>> =
        new Map<MapObjectType, Array<google.maps.Marker>>();

    private selectedMapObject: MapObject;
    private selectedMapObjectType: MapObjectType;
    private selectedMarker: google.maps.Marker;

    @ViewChild("mapCanvas") private mapCanvas;

    constructor(private mapService: MapService, private zone: NgZone) {
        this.initializeMarkerMap();
        this.initializeMapObjectSettings();
    }

    public ngAfterViewInit() {
        this.initMap();
        this.retrieveVisibleMapObjects();
    }

    public onCheckboxChange() {
        this.retrieveVisibleMapObjects();
        this.deleteNotVisibleMapObjects();
    }

    private initMap() {
        const latlng = new google.maps.LatLng(51.0679567, 13.5767141);
        const mapOptions = {
            center: latlng,
            scrollWheel: false,
            zoom: 10,
            zoomControl: true,
            mapTypeControl: false,
            streetViewControl: false,
        };
        this.map = new google.maps.Map(this.mapCanvas.nativeElement, mapOptions);
        this.map.addListener("click", () =>  this.updateSelectedMapObjectInfo(null, null, null));
    }

    private retrieveVisibleMapObjects() {
        this.updateSelectedMapObjectInfo(null, null, null);
        for (let mapObjectType of this.mapObjectTypes) {
            if (this.mapObjectSettings[mapObjectType].visible) {
                this.mapService.getMapObjects(mapObjectType)
                            .subscribe(
                                mapObjects => this.drawMapObjects(mapObjects, mapObjectType),
                                error => this.setErrorMessage(<any> error)
                            );
            }
        }
    }

    private drawMapObjects(mapObjects: MapObject[], mapObjectType: MapObjectType) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject, mapObjectType));
    }

    private drawMapObject(mapObject: MapObject, mapObjectType: MapObjectType) {
        const latLng = new google.maps.LatLng(mapObject.locationLat, mapObject.locationLong);
        const marker = new google.maps.Marker({
            position: latLng,
            title: mapObject.name,
            icon: this.mapObjectSettings[mapObjectType].iconPath,
        });

        marker.addListener("click", (() => {
            this.updateSelectedMapObjectInfo(mapObject, mapObjectType, marker);
            if (this.willInfoBoxHideMarker(marker)) {
                this.map.panTo(marker.getPosition());
            }
        }));
        marker.setMap(this.map);
        this.markers.get(mapObjectType).push(marker);
    }

    private initializeMapObjectSettings() {
        this.mapObjectSettings[MapObjectType.EVENTS] =
            new MapObjectSetting(true, "static/img/schild_schwarz.png", "static/img/schild_aktiv_schwarz.png",
                "Veranstaltungen");
        this.mapObjectSettings[MapObjectType.FACEBOOK_PAGES] =
            new MapObjectSetting(false, "static/img/facebook.png", "static/img/facebook_aktiv.png",
                "Facebook-Seiten");
    }

    private initializeMarkerMap() {
        for (let mapObjectType of this.mapObjectTypes) {
            this.markers.set(mapObjectType, new Array<google.maps.Marker>());
        }
    }

    private deleteNotVisibleMapObjects() {
        for (let mapObjectType of this.mapObjectTypes) {
            if (!this.mapObjectSettings[mapObjectType].visible && this.markers.get(mapObjectType).length > 0) {
                for (let marker of this.markers.get(mapObjectType)) {
                    marker.setMap(null);
                }
                this.markers.set(mapObjectType, new Array<google.maps.Marker>());
            }
        }
    }

    private updateSelectedMapObjectInfo(mapObject: MapObject, mapObjectType: MapObjectType,
                                        marker: google.maps.Marker) {
        this.zone.run(() => {
            if (this.selectedMarker) {
                this.selectedMarker.setIcon(this.mapObjectSettings
                    [this.selectedMapObjectType].iconPath);
            }

            if (marker) {
                marker.setIcon(this.mapObjectSettings[mapObjectType].iconClickedPath);
            }

            this.selectedMapObject = mapObject;
            this.selectedMapObjectType = mapObjectType;
            this.selectedMarker = marker;
        });
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
        const tmpScope = this;
        setTimeout(function(){
            tmpScope.errorMessage = "";
        }, this.errorMessageDisplayTime);
    }

    private willInfoBoxHideMarker(marker: google.maps.Marker) {
        const infoBoxWidth = 320; // incl. padding
        const windowWidth = this.mapCanvas.nativeElement.clientWidth;

        const longitudeWest = this.map.getBounds().getSouthWest().lng();
        const longitudeEast = this.map.getBounds().getNorthEast().lng();
        const mapWidth = longitudeEast - longitudeWest;
        const markerLngRelative = marker.getPosition().lng() - longitudeWest;

        // We compare the ratio of the width of info box and window with the ratio of the longitude
        // of the marker (realtive to the left border of the map) and the range of shown longitude of the map.
        return (infoBoxWidth / windowWidth) > (markerLngRelative / mapWidth);
    }
}
