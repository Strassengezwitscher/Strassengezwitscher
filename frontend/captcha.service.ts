import { Injectable }     from "@angular/core";
import { Http, Response, Headers, RequestOptions } from "@angular/http";
import { Observable }     from "rxjs/Observable";

@Injectable()
export class CaptchaService {

    private captchaUrl = "api/captcha/";

    constructor(private http: Http) {}

    public validateCaptcha (response: any): Observable<Response> {

    let body = JSON.stringify({ response });
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    console.log(body)
    return this.http.post(this.captchaUrl, body, options)
                    .map(this.handleReponse)
                    .catch(this.handleError);
    }

    private handleReponse(response: Response) {
        console.log("Success");
        return response.json();
    }

    private handleError(error: any) {
        console.log("Error");
        let errorMessage = "Server error";
        if (error.message) {
            errorMessage = error.message;
        } else if (error.status) {
            errorMessage = `${error.status} - ${error.statusText}`;
        }
        console.error(errorMessage);
        return Observable.throw(errorMessage);
    }
}
