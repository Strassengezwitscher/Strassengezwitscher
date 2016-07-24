export class Contact {

    constructor(
        public name: string,
        public email: string,
        public subject: string,
        public message: string,
        public journalist: boolean,
        public confidential: boolean,
        public files: any
    ) { }
}
