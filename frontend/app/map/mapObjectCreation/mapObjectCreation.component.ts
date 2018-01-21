import { Component, Output, EventEmitter, Input, OnInit, NgZone, OnDestroy } from "@angular/core";

import { MapService } from "../map.service";
import { MapObjectType } from "../mapObject.model";
import { CaptchaService } from "../../captcha/captcha.service";
import { Config } from "../../../config/config";
import { FacebookPageService } from "../../facebook/facebookPage.service";
import { FacebookPage } from "../../facebook/facebookPage.model";
import { EventService } from "../../events/shared/event.service";
import { Event } from "../../events/shared/event.model";

@Component({
    moduleId: module.id,
    selector: "cg-map-object-creation",
    templateUrl: "mapObjectCreation.component.html",
    styleUrls: ["mapObjectCreation.component.css"],
})
export class MapObjectCreationComponent implements OnInit, OnDestroy {
    @Output() public onError = new EventEmitter<string>();
    @Output() public onSuccess = new EventEmitter<string>();
    @Output() public onDestroy = new EventEmitter<boolean>();
    @Input("map") public map: google.maps.Map;
    @Input("mapObjectType") selectedMapObjectType: MapObjectType;
    public mapObjectType = MapObjectType;
    public marker = null;
    public captchaVerified;
    public config: Config;
    public userAgentIsChrome = true;
    private script;
    constructor(private mapService: MapService, private captchaService: CaptchaService,
                private fbPageService: FacebookPageService, private eventService: EventService,
                private zone: NgZone) {
        this.config = new Config();
        this.captchaVerified = false;
        this.userAgentIsChrome = window.navigator.userAgent.indexOf("Chrome/") !== -1;  // hide tooltip on chrome
        window["verifyCallback"] = this.verifyCallback.bind(this);
    }

    public moveMarker(location) {
        if ( this.marker == null ) {
            this.marker = new google.maps.Marker({
                position: location,
                map: this.map,
            });
            this.toggleMarkerColor(true);
            this.marker.addListener("click", () => {
                this.zone.run(() => {
                    this.marker.setMap(null);
                    this.marker = null;
                    this.toggleMarkerColor(false);
                });
            });
        } else {
            this.marker.setPosition(location);
        }
    }

    public ngOnInit() {
        google.maps.event.clearListeners(this.map, "click");
        this.appendCaptchaScript();
        google.maps.event.addListener(this.map, "click", (event) => {
            this.zone.run(() => {
                this.moveMarker(event.latLng);
            });
        });
    }

    public setType(type: MapObjectType) {
        this.selectedMapObjectType = type
    }

    public send(moc) {
        switch (this.selectedMapObjectType) {
            case MapObjectType.EVENTS:
                let date;
                if (this.userAgentIsChrome) {
                    date = moc.form._value.date;
                } else {
                    date = moc.form._value.date + "T" + moc.form._value.time;
                }

                // TODO constructing event should be changed with JSONAPI
                let event = new Event();
                event.counterEvent = (moc.form.controls.counterEvent.touched) ?  moc.form._value.counterEvent : false;
                event.date = date;
                event.time = date;
                event.location = moc.form._value.location;
                event.locationLat = moc.form._value.locationLat;
                event.locationLong = moc.form._value.locationLong;
                event.name = moc.form._value.name;
                event.organizer = moc.form._value.organizer;
                event.participants = moc.form._value.participants;
                event.repetitionCycle = (moc.form._value.repetitionCycle != '') ? moc.form._value.repetitionCycle : 'Unbekannter Rhytmus';
                event.type = moc.form._value.type;
                event.url = moc.form._value.url;
                this.eventService.addEvent(event).subscribe(
                       res  => this.successfulResponse(res, moc),
                       error =>  this.onError.emit(error));
                break;
            case MapObjectType.FACEBOOK_PAGES:
                // TODO constructing fbPage should be changed with JSONAPI
                let fbPage = new FacebookPage();
                fbPage.facebookId = moc.form._value.facebookId;
                fbPage.location = moc.form._value.location;
                fbPage.locationLat =  moc.form._value.locationLat;
                fbPage.locationLong =  moc.form._value.locationLong;
                fbPage.name =  moc.form._value.name;
                fbPage.notes =  moc.form._value.notes;
                this.fbPageService.addFacebookPage(fbPage).subscribe(
                       res  => this.successfulResponse(res, moc),
                       error =>  this.onError.emit(error));
                break;
            default:
                this.onError.emit("Keine valide Kategorie gewählt");
        }
    }

    public ngOnDestroy() {
        this.removeCaptchaScript();
        this.removeMarker();
        google.maps.event.clearListeners(this.map, "click");
        this.onDestroy.emit(true);
    }

    public verifyCallback(response) {
        this.captchaService.validateCaptcha(response).subscribe((data) => this.verifiedCaptcha(),
                                                                (err) => this.onError.emit(err));
    }

    public verifiedCaptcha() {
        // zone required to allow Angular to update variable
        this.zone.run(() => {
            this.captchaVerified = true;
        });
    }

    public changeMarkerLat(lat) {
        if (this.marker == null) {
            this.moveMarker({"lat": Number(lat), "lng": 0.0});
        } else {
            this.moveMarker({"lat": Number(lat), "lng": this.marker.position.lng()});
        }

    }

    public changeMarkerLng(lng) {
        if (this.marker == null) {
            this.moveMarker({"lat": 0.0, "lng": Number(lng)});
        } else {
            this.moveMarker({"lat": this.marker.position.lat(), "lng": Number(lng)});
        }
    }

    private successfulResponse(res, moc) {
        this.onSuccess.emit(res);
        this.removeMarker();
        this.clearForm(moc);
    }

    private clearForm(moc) {
        moc.reset();
        this.selectedMapObjectType = null;
    }

    private removeMarker() {
        if (this.marker != null) {
            this.marker.setMap(null);
            this.marker = null;
        }
    }

    private removeCaptchaScript() {
        this.script.parentNode.removeChild(this.script);
    }

    private appendCaptchaScript() {
        let doc = <HTMLDivElement> document.body;
        this.script = document.createElement("script");
        this.script.innerHTML = "";
        this.script.src = "https://www.google.com/recaptcha/api.js";
        this.script.async = true;
        this.script.defer = true;
        doc.appendChild(this.script);
    }

    private toggleMarkerColor(colored: boolean) {
        const toggle = document.getElementById("markerToggle");
        const bar = <HTMLElement>toggle.querySelector(".md-slide-toggle-bar");
        const thumb = <HTMLElement>toggle.querySelector(".md-slide-toggle-thumb");

        if (colored) {
            bar.style.backgroundColor = "rgba(156, 39, 176, 0.5)";
            thumb.style.backgroundColor = "#9c27b0";
        } else {
            bar.style.backgroundColor = "rgba(0, 0, 0, 0.1)";
            thumb.style.backgroundColor = "#bdbdbd";
        }
    }

}
