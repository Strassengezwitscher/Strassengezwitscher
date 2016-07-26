import { Component }      from "@angular/core";
import { Router }         from "@angular/router";

import { ContactService } from "./contact.service";
import { Contact }        from "./contact";

import { TOOLTIP_DIRECTIVES } from "ng2-bootstrap/components/tooltip";

@Component({
    selector: "sg-contact",
    templateUrl: "contact.component.html",
    providers: [ContactService],
    directives: [TOOLTIP_DIRECTIVES],
})
export class ContactComponent {

    private contactErrorMessage: string;
    private contact: Contact;
    private uploads: FileList;
    private maxFileNameLength = 50;
    private filesValid = true;

    constructor( private contactService: ContactService, private router: Router) {
        this.contact = new Contact("", "", "", "", null, null);
        this.filesValid = true;
    }

    public onFileChange(event) {
        let errorMessage = "";
        for (let i = 0; i < event.srcElement.files.length; ++i) {
            if (event.srcElement.files[i].name.length > this.maxFileNameLength) {
                errorMessage += "Name des Anhangs '" + event.srcElement.files[i].name +
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
        this.contactService.addContactData(this.contact, this.uploads).subscribe((data) =>
                                            this.router.navigate([""]), (err) => this.displayError(err));
    }

    public clearError() {
        this.contactErrorMessage = "";
    }

    private displayError(err: any) {
        this.contactErrorMessage = "Fehler bei der Kontaktaufnahme: \n";
        if (err.status === 400) {
            for (let key in err.error.errors) {
                if (err.error.errors.hasOwnProperty(key)) {
                    this.contactErrorMessage += key + ": " + err.error.errors[key] + " \n";
                }
            }
        } else {
            this.contactErrorMessage += "Interner Fehler, " + err.error.errors;
        }
    }

}
