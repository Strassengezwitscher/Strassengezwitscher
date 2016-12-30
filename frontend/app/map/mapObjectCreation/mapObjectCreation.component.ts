import { Component, Output, EventEmitter, OnInit, NgZone, OnDestroy } from "@angular/core";

import { MapService } from "../map.service";
import { MapObjectType, MapObjectTypeNaming } from "../mapObject.model";
import { CaptchaService } from "../../captcha/captcha.service";
import { Config } from "../../../config/config";

@Component({
    moduleId: module.id,
    selector: "cg-map-object-creation",
    templateUrl: "mapObjectCreation.component.html",
    styleUrls: ["mapObjectCreation.component.css"],
})
export class MapObjectCreationComponent implements OnInit, OnDestroy {
    @Output() public onError = new EventEmitter<string>();
    public selectedMapObjectType: MapObjectType;
    public mapObjectType = MapObjectType;
    public mapObjectTypes = MapObjectTypeNaming;
    public currentTime = new Date();
    private captchaVerified;
    private script;
    private config: Config;
    constructor(private mapService: MapService, private captchaService: CaptchaService,
                private zone: NgZone) {
        this.captchaVerified = false;
        this.config = new Config();
        window["verifyCallback"] = this.verifyCallback.bind(this);
    }

    public send(moc) {
        console.log(this.selectedMapObjectType);
        console.log(moc);
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
