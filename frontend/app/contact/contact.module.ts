import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { MaterialModule } from "@angular/material";

import { ContactComponent } from "./contact.component";
import { ContactService } from "./contact.service";
import { CaptchaModule } from "../captcha/captcha.module";
import { routing } from "./contact.routing";

@NgModule({
  imports: [MaterialModule, BrowserModule, FormsModule, CaptchaModule, routing],
  declarations: [ContactComponent],
  providers: [ContactService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class ContactModule {}
