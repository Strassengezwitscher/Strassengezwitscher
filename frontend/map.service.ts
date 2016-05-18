import { Injectable } from "@angular/core";

import { TWEETS } from "./mock-tweets";

@Injectable()
export class MapService {
    getTweets() {
        return Promise.resolve(TWEETS);
    }
}
