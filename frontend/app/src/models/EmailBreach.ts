import { Breach } from "./Breach";

export interface EmailBreach {
    email: string;
    breaches: [Breach];
}