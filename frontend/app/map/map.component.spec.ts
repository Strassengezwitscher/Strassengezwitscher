import { BaseRequestOptions, Http } from "@angular/http";
import { MockBackend } from "@angular/http/testing";
import { NgZone } from "@angular/core";

import { MapObjectType, MapStateType } from "./mapObject.model";
import { MapComponent } from "./map.component";
import { MapService } from "./map.service";

describe("MapComponent", () => {

    beforeEach(() => {
        this.mapComponent = new MapComponent(new MapService(new Http(new MockBackend(), new BaseRequestOptions())),
                                             new NgZone(true));
    });

    it("Should set the selectedMapObjectInfo to null, when the infobox is cleared", done => {
        this.mapComponent.clearInfoBox();
        expect(this.mapComponent.selectedMapObject).toEqual(null);
        expect(this.mapComponent.selectedMapObjectType).toEqual(null);
        expect(this.mapComponent.selectedMarker).toEqual(null);
        done();
    });

    it("Should have an initialized markerMap and mapObjectSettings after construction", done => {
        expect(this.mapComponent.markers.size).toBe(this.mapComponent.mapObjectTypes.length);
        for (let mapObjectType of this.mapComponent.mapObjectTypes) {
            expect(this.mapComponent.markers.get(mapObjectType).length).toBe(0);
            expect(this.mapComponent.markers.get(mapObjectType) instanceof Array).toBeTruthy();
        }

        expect(this.mapComponent.mapObjectSettings.length).toBe(this.mapComponent.mapObjectTypes.length);

        done();
    });

    it("Should retrieve visible objects and delete not visible ones onCheckboxChange", done => {
        spyOn(this.mapComponent, "deleteNotVisibleMapObjects");
        spyOn(this.mapComponent, "retrieveVisibleMapObjects");

        // The point is that deleteNotVisibleMapObjects gets called each time when onCheckboxChange is triggered,
        // but retrieveVisibleMapObjects will only be called if there is only one filter option (FACEBOOK_PAGES)

        this.mapComponent.onCheckboxChange(this.mapComponent.mapObjectSettings[MapObjectType.FACEBOOK_PAGES]);
        expect(this.mapComponent.deleteNotVisibleMapObjects).toHaveBeenCalledTimes(1);
        expect(this.mapComponent.retrieveVisibleMapObjects).toHaveBeenCalledTimes(1);

        this.mapComponent.onCheckboxChange(this.mapComponent.mapObjectSettings[MapObjectType.EVENTS]);
        expect(this.mapComponent.deleteNotVisibleMapObjects).toHaveBeenCalledTimes(2);
        expect(this.mapComponent.retrieveVisibleMapObjects).toHaveBeenCalledTimes(2);

        done();
    });

    it("Should set the mapState to Adding", done => {
        this.mapComponent.showFormForMapObject(MapObjectType.EVENTS);
        expect(this.mapComponent.mapState).toEqual(MapStateType.ADDING);
        done();
    });

    it("Should set the mapState to Viewing", done => {
        this.mapComponent.successfulMapObjectCreation("successful MapObject creation");
        expect(this.mapComponent.mapState).toEqual(MapStateType.VIEWING);
        expect(this.mapComponent.successMessage).toEqual("successful MapObject creation");
        done();
    });

    it("Should set the successMessage", done => {
        this.mapComponent.setSuccessMessage("Test Nachricht");
        expect(this.mapComponent.successMessage).toEqual("Test Nachricht");
        done();
    });

});
