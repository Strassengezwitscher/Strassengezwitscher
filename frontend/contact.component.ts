import { Component }      from "@angular/core";
import { Router }         from "@angular/router";
// TODO (Chris) integrate Captcha properly: import {ReCaptchaComponent} from 'angular2-recaptcha/angular2-recaptcha';

import { ContactService } from "./contact.service";
import { Contact }        from "./contact";

@Component({
    selector: "sg-contact",
    templateUrl: "contact.component.html",
    providers: [ContactService],
    // TODO (Chris) integrate Captcha properly:  directives: [ReCaptchaComponent]
})
export class ContactComponent {
    public contact = new Contact("", "", "", "", null, null, null);
    constructor( private contactService: ContactService, private router: Router) {}

    public onFileChange(event) {
        this.contact.files = event.srcElement.files;
    }

    public onSubmit() {
        this.contactService.addContactData(this.contact).subscribe((data) =>
                                            this.router.navigate([""]), (err) => this.displayError(err));
    }

    private displayError(err: any) {
        // TODO (Chris) handle error codes
        console.log(err);
    }
}
