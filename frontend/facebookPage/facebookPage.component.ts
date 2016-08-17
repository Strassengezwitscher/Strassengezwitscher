import { Component, Input, OnChanges } from "@angular/core";

import { FacebookPage } from "./facebookPage";
import { FacebookPageService } from "./facebookPage.service";

@Component({
    moduleId: module.id,
    selector: "cg-fb-detail",
    templateUrl: "facebookPage.component.html",
    providers: [FacebookPageService],
})

export class FacebookPageComponent implements OnChanges {
    private activePage: FacebookPage;
    @Input("id") private id: number;
    constructor(private fbPageService: FacebookPageService) {
        this.activePage = new FacebookPage();
    }

    public ngOnChanges(changes) {
        if (changes.id !== undefined) {
            this.getFacebookPageDetails(this.id);
        }
    }

    private getFacebookPageDetails(id: number) {
        this.fbPageService.getFacebookPage(id)
                            .subscribe(
                                fbPage => this.setActivePage(fbPage),
                                error => console.log(error)
                            );
    }

    private setActivePage(fbPage: FacebookPage) {
        this.activePage = fbPage;
    }
}
