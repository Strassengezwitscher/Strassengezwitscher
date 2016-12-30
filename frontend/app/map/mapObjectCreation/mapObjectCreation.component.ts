import { Component, Output, EventEmitter, OnInit, NgZone, OnDestroy } from "@angular/core";

import { MapService } from "../map.service";
import { MapObjectType, MapObjectTypeNaming } from "../mapObject.model";
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
    public selectedMapObjectType;
    public mapObjectType = MapObjectType;
    public mapObjectTypes = MapObjectTypeNaming;
    public currentTime = new Date();
    private captchaVerified;
    private script;
    private config: Config;
    constructor(private mapService: MapService, private captchaService: CaptchaService,
                private fbPageService: FacebookPageService, private eventService: EventService,
                private zone: NgZone) {
        this.captchaVerified = false;
        this.config = new Config();
        window["verifyCallback"] = this.verifyCallback.bind(this);
    }

    public send(moc) {
        switch (parseInt(this.selectedMapObjectType, 10)) {
            case MapObjectType.EVENTS:
                // TODO construct correct event here
                let event = new Event();
                this.eventService.addEvent(event).subscribe(
                       res  => this.onSuccess.emit(res),
                       error =>  this.onError.emit(error));
                break;
            case MapObjectType.FACEBOOK_PAGES:
                // TODO construct correct fbPage here
                let fbPage = new FacebookPage();
                this.fbPageService.addFacebookPage(fbPage).subscribe(
                       res  => this.onSuccess.emit(res),
                       error =>  this.onError.emit(error));
                break;
            default:
                this.onError.emit("Keine valide Kategorie gewählt");
        }
    }

    public ngOnInit() {
        // Add script tag manually as it does not work from frontend.html, g-recaptcha not displayed
        this.appendCaptchaScript();
    }

    public ngOnDestroy() {
        this.removeCaptchaScript();
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

}
