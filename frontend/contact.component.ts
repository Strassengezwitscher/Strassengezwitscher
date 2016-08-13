import { Component, OnInit, NgZone, OnDestroy } from "@angular/core";
import { Router } from "@angular/router";
import { ContactService } from "./contact.service";
import { Contact } from "./contact";
import { CaptchaService } from "./captcha.service";
import { ConfigurationService } from "./config.service";
import { TOOLTIP_DIRECTIVES } from "ng2-bootstrap/components/tooltip";

@Component({
    selector: "cg-contact",
    templateUrl: "contact.component.html",
    providers: [ContactService, CaptchaService, ConfigurationService],
    directives: [TOOLTIP_DIRECTIVES],
})
export class ContactComponent implements OnInit, OnDestroy {
    private contactErrorMessage: string;
    private contactSuccessMessage: string;
    private contact: Contact;
    private uploads: FileList;
    private maxFileNameLength = 50;
    private filesValid;
    private captchaVerfied;
    private script;
    private grecaptchaKey;

    constructor( private contactService: ContactService, private captchaService: CaptchaService,
                 private configService: ConfigurationService, private router: Router, private zone: NgZone) {
        this.contact = new Contact("", "", "", "", null, null);
        this.filesValid = true;
        this.captchaVerfied = false;
        window["verifyCallback"] = this.verifyCallback.bind(this);
        this.grecaptchaKey = this.configService.getConfigEntry("data-sitekey");
    }

    public ngOnInit() {
        // Add script tag manually as it does not work from frontend.html, g-recaptcha not displayed
        let doc = <HTMLDivElement> document.body;
        this.script = document.createElement("script");
        this.script.innerHTML = "";
        this.script.src = "https://www.google.com/recaptcha/api.js";
        this.script.async = true;
        this.script.defer = true;
        doc.appendChild(this.script);
    }

    public ngOnDestroy() {
        this.script.parentNode.removeChild(this.script);
    }

    public onFileChange(event) {
        let errorMessage = "";

        for (let file of event.srcElement.files) {
            if (file.name.length > this.maxFileNameLength) {
                errorMessage += "Name des Anhangs '" + file.name +
                                "' zu lang (maximal 50 Zeichen)\n";
            }
        }
        if (errorMessage) {
            this.filesValid = false;
            this.contactErrorMessage = errorMessage;
        } else {
            this.filesValid = true;
            this.uploads = event.srcElement.files;
        }
    }

    public onSubmit() {
        this.contactService.addContactData(this.contact, this.uploads).subscribe((data) => this.displaySuccess(),
                                            (err) => this.displayError(err));
    }

    public clearError() {
        this.contactErrorMessage = "";
    }

    public verifyCallback(response) {
        this.captchaService.validateCaptcha(response).subscribe((data) => this.verifiedCaptcha(),
                                                                (err) => this.displayError(err));
    }

    public verifiedCaptcha() {
        // zone required to allow Angular to update variable
        this.zone.run(() => {
            this.captchaVerfied = true;
        });
    }

    private displaySuccess() {
        this.contactSuccessMessage = "Vielen Dank! Wir werden Ihre Anfrage schnellstmöglich bearbeiten!";
        let tmpScope = this;
        setTimeout(function(){
            tmpScope.contactSuccessMessage = "";
            tmpScope.router.navigate([""]);
        }, 4000);
    }

    private displayError(errorMessage: string) {
        this.contactErrorMessage = errorMessage;
    }
}
