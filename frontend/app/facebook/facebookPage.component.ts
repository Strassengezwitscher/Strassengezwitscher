import { Component, EventEmitter, Input, OnChanges, Output } from "@angular/core";

import { FacebookPage } from "./facebookPage.model";
import { FacebookPageService } from "./facebookPage.service";

@Component({
    moduleId: module.id,
    selector: "cg-fb-detail",
    templateUrl: "facebookPage.component.html",
    styleUrls: ["facebookPage.component.css"],
})

export class FacebookPageComponent implements OnChanges {
    public activePage: FacebookPage;
    @Input("id") public id: number;
    @Output() public onError = new EventEmitter<string>();
    @Output() public onClose = new EventEmitter<boolean>();
    constructor(private fbPageService: FacebookPageService) {
        this.activePage = new FacebookPage();
    }

    public ngOnChanges(changes) {
        if (changes.id !== undefined) {
            this.getFacebookPageDetails(this.id);
        }
    }

    public close() {
        this.onClose.emit(true);
    }

    private getFacebookPageDetails(id: number) {
        this.fbPageService.getFacebookPage(id)
                            .subscribe(
                                fbPage => this.setActivePage(fbPage),
                                error => this.onError.emit(error)
                            );
    }

    private setActivePage(fbPage: FacebookPage) {
        this.activePage = fbPage;
    }
}
