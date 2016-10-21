import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { FacebookPageComponent } from "./facebookPage.component";
import { FacebookPageService } from "./facebookPage.service";

@NgModule({
  imports: [BrowserModule],
  declarations: [FacebookPageComponent],
  exports: [FacebookPageComponent],
  providers: [FacebookPageService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class FacebookPageModule {}
