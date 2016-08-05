import { Component } from "@angular/core";
import { Router } from "@angular/router";
import { MD_INPUT_DIRECTIVES } from "@angular2-material/input/input";
import { MdButton } from "@angular2-material/button/button";
import { MdCard } from "@angular2-material/card/card";
import { MdCheckbox } from "@angular2-material/checkbox/checkbox";

import { ContactService } from "./contact.service";
import { Contact }        from "./contact";


@Component({
    selector: "sg-contact",
    templateUrl: "contact.component.html",
    providers: [ContactService],
    directives: [
        MdCard,
        MdCheckbox,
        MdButton,
        MD_INPUT_DIRECTIVES,
    ],
})
export class ContactComponent {
    private contactErrorMessage: string;
    private contactSuccessMessage: string;
    private contact: Contact;
    private uploads: FileList;
    private maxFileNameLength = 50;
    private filesValid = true;
    private fileInputNames = "";

    constructor( private contactService: ContactService, private router: Router) {
        this.contact = new Contact("", "", "", "", null, null);
        this.filesValid = true;
    }

    public onFileChange(event) {
        let errorMessage = "";
        let fileNames: String[] = [];

        for (let file of event.srcElement.files) {
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
            this.uploads = event.srcElement.files;
            this.fileInputNames = fileNames.join(", ");
            console.log(this.fileInputNames, fileNames)
        }
    }

    public onSubmit() {
        this.contactService.addContactData(this.contact, this.uploads).subscribe((data) => this.displaySuccess(),
                                            (err) => this.displayError(err));
    }

    public clearError() {
        this.contactErrorMessage = "";
    }

    public displaySuccess() {
        this.contactSuccessMessage = "Vielen Dank! Wir werden Ihre Anfrage schnellstmöglich bearbeiten!";
        let tmpScope = this;
        setTimeout(function(){
            tmpScope.contactSuccessMessage = "";
            tmpScope.router.navigate([""]);
        }, 4000);
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
