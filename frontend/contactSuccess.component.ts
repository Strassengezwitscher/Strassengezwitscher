import { Component } from "@angular/core";

@Component({
    moduleId: module.id,
    selector: "cg-contact-success",
    templateUrl: "contactSuccess.component.html",
})
export class ContactSuccessComponent {
    private contactSuccessMessage: string;

    constructor() {
        this.contactSuccessMessage = "Vielen Dank! Wir werden Ihre Anfrage schnellstmöglich bearbeiten!";
    }

}
