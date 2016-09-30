import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { HttpModule } from "@angular/http";
import { MaterialModule } from "@angular/material";

import { AppComponent } from "./app.component";
import { AppRouterModule } from "./app.routing";

import { AboutModule } from "./about/about.module";
import { BlogModule } from "./blog/blog.module";
import { ContactModule } from "./contact/contact.module";
import { EventModule } from "./events/event.module";
import { FacebookPageModule } from "./facebook/facebookPage.module";
import { ImprintModule } from "./imprint/imprint.module";
import { MapModule } from "./map/map.module";

@NgModule({
    imports: [
        BrowserModule,
        HttpModule,
        AppRouterModule,
        MaterialModule.forRoot(),
        AboutModule,
        BlogModule,
        ContactModule,
        EventModule,
        FacebookPageModule,
        ImprintModule,
        MapModule,
    ],
    declarations: [AppComponent],
    entryComponents: [AppComponent],
    bootstrap: [AppComponent],
    schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class AppModule {}
