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

    constructor( private contactService: ContactService, private router: Router) {
        this.contact = new Contact("", "", "", "", null, null);
    }

    public onFileChange(event) {
        this.uploads = event.srcElement.files;
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
