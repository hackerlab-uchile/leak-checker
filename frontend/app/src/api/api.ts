import { DataLeak } from "@/models/Breach";
import { ErrorMsg } from "@/models/ErrorMsg";
import { SearchQuery } from "@/models/SearchQuery";
import { User } from "@/models/User";
import { VerificationResponse } from "@/models/VerificationResponse";
import apiClient from "@/utils/axios";

export enum QueryType {
  Email = "email",
  Rut = "rut",
  Phone = "phone",
}

export async function getDataLeaksByValueAndType(
  data: SearchQuery
): Promise<[DataLeak[], boolean]> {
  let response;
  let got_error: boolean = false;
  try {
    response = await apiClient.post<DataLeak[]>("/breach/data/", data, {
      withCredentials: true,
    });
    return [response.data, got_error];
  } catch (error: any) {
    got_error = true;
    if (error.response && error.response.status === 404) {
      return [[], got_error];
    } else {
      // TODO: Informar que ha ocurrido un error
      return [[], got_error];
      // throw error;
    }
  }
}

export async function getDataLeaksByValueAndTypeDemo(
  data: SearchQuery
): Promise<[DataLeak[], boolean]> {
  let response;
  let got_error: boolean = false;
  try {
    response = await apiClient.post<DataLeak[]>("/demo/data/", data, {
      withCredentials: true,
    });
    return [response.data, false];
  } catch (error: any) {
    got_error = true;
    if (error.response && error.response.status === 404) {
      return [[], got_error];
    } else {
      // TODO: Informar que ha ocurrido un error
      return [[], got_error];
      // throw error;
    }
  }
}

export async function sendVerificationEmail(
  query: string
): Promise<VerificationResponse> {
  let response;
  const data = { email: query };
  try {
    response = await apiClient.post<VerificationResponse>(
      `/verify/send/email/`,
      data
    );
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.status === 422) {
      return {
        message:
          "El formato del correo ingresado no es válido. Por favor, inténtelo de nuevo",
      };
    } else if (error.response && error.response.status === 429) {
      return {
        message:
          "Se han realizado demasiadas solicitudes. Inténtelo de nuevo más tarde",
      };
    } else {
      return {
        message: "Ha ocurrido un error. Por favor, inténtelo más tarde",
      };
    }
  }
}

export async function sendVerificationSMS(
  query: string
): Promise<VerificationResponse> {
  let response;
  const data = { phone: query };
  try {
    response = await apiClient.post(`/verify/send/sms/`, data);
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.status === 422) {
      return {
        message:
          "El formato del número móvil ingresado no es válido. Por favor, inténtelo de nuevo",
      };
    } else if (error.response && error.response.status === 429) {
      return {
        message:
          "Se han realizado demasiadas solicitudes. Inténtelo de nuevo más tarde",
      };
    } else {
      return {
        message: "Ha ocurrido un error. Por favor, inténtelo más tarde",
      };
    }
  }
}

export async function verifyCode(
  code: string,
  value: string,
  type: QueryType
): Promise<[boolean, string]> {
  let response;
  const data = { code: code, value: value, dtype: type };
  try {
    response = await apiClient.post(`/verify/code/`, data, {
      withCredentials: true,
    });
    let isValid = response.data.valid;
    console.log("Response: ", isValid);
    return [isValid, ""];
  } catch (error: any) {
    return [false, "Ha ocurrido un error. Por favor, inténtelo más tarde"];
  }
}

export async function getSensitiveDataLeaks(): Promise<[DataLeak[], ErrorMsg]> {
  let response;
  let errorMsg: ErrorMsg = { statusCode: 200, message: "" };
  try {
    response = await apiClient.get<DataLeak[]>("/breach/sensitive/data/", {
      withCredentials: true,
    });
    return [response.data, errorMsg];
  } catch (error: any) {
    if (error.response) {
      errorMsg.statusCode = error.response.status;
    }
    errorMsg.message = "Credenciales inválidas";
    return [[], errorMsg];
  }
}

export async function getSensitiveDataLeaksDemo(): Promise<
  [DataLeak[], ErrorMsg]
> {
  let response;
  let errorMsg: ErrorMsg = { statusCode: 200, message: "" };
  try {
    response = await apiClient.get<DataLeak[]>("/demo/data/sensitive/", {
      withCredentials: true,
    });
    return [response.data, errorMsg];
  } catch (error: any) {
    if (error.response) {
      errorMsg.statusCode = error.response.status;
    }
    errorMsg.message = "Credenciales inválidas";
    return [[], errorMsg];
  }
}

export async function get_current_user(): Promise<[User | null, ErrorMsg]> {
  let errorMsg: ErrorMsg = { statusCode: 200, message: "" };
  try {
    let response = await apiClient.get<User>("/user/me/", {
      withCredentials: true,
    });
    return [response.data, errorMsg];
  } catch (error: any) {
    if (error.response) {
      errorMsg.statusCode = error.response.status;
    }
    errorMsg.message = "Credenciales inválidas";
    return [null, errorMsg];
  }
}

export async function logout_user() {
  let errorMsg: ErrorMsg = { statusCode: 200, message: "" };
  try {
    let response = await apiClient.get("/user/logout/", {
      withCredentials: true,
    });
    return [response.data, errorMsg];
  } catch (error: any) {
    if (error.response) {
      errorMsg.statusCode = error.response.status;
    }
    errorMsg.message = "Credenciales inválidas";
    return [null, errorMsg];
  }
}
