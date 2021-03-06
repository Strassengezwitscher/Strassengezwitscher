import { Component, OnInit, NgZone, OnDestroy } from "@angular/core";
import { Router } from "@angular/router";

import { Contact } from "./contact.model";
import { ContactService } from "./contact.service";
import { CaptchaService } from "../captcha/captcha.service";
import { Config } from "../../config/config";

@Component({
    moduleId: module.id,
    selector: "cg-contact",
    templateUrl: "contact.component.html",
    styleUrls: ["contact.component.css"],
})
export class ContactComponent implements OnInit, OnDestroy {
    public contactErrorMessage: string;
    public contactSuccessMessage: string;
    private contact: Contact;
    private config: Config;
    private uploads: FileList;
    private maxFileNameLength = 50;
    private filesValid;
    private fileInputNames;
    private captchaVerified;
    private script;

    private isMessageInputFocused = false;

    constructor( private contactService: ContactService, private captchaService: CaptchaService,
                 private router: Router, private zone: NgZone) {
        this.config = new Config();
        this.contact = new Contact("", "", "", "", false, false);
        this.filesValid = true;
        this.captchaVerified = false;
        this.fileInputNames = "";
        window["verifyCallback"] = this.verifyCallback.bind(this);
    }

    public ngOnInit() {
        // Add script tag manually as it does not work from frontend.html, g-recaptcha not displayed
        this.appendCaptchaScript();
    }

    public ngOnDestroy() {
        this.removeCaptchaScript();
    }

    public onFileChange(event) {
        let errorMessage = "";
        let fileNames: String[] = [];
        let target = event.target || event.srcElement;

        for (let file of target.files) {
            fileNames.push(file.name);
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
            this.uploads = target.files;
            this.fileInputNames = fileNames.join(", ");
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
            this.captchaVerified = true;
        });
    }

    public blurMessageInput() {
        this.isMessageInputFocused = (this.contact.message !== "");
    }

    public resetContactForm() {
        this.resetContact();
        this.clearError();
        this.contactSuccessMessage = "";
        this.clearFileUpload();
        this.captchaVerified = false;
        this.removeCaptchaScript();
        this.appendCaptchaScript();
    }

    private clearFileUpload() {
        this.fileInputNames = "";
        this.uploads = null;
    }

    private resetContact() {
        this.contact = new Contact("", "", "", "", false, false);
    }

    private displaySuccess() {
        this.clearError();
        this.contactSuccessMessage = "Vielen Dank! Wir werden Ihre Anfrage schnellstmöglich bearbeiten!";
    }

    private displayError(errorMessage: string) {
        this.contactErrorMessage = errorMessage;
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
