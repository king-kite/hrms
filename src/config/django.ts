const ROOT_URL = "/api";

// Authentication and User Information URLs
export const LOGIN_URL = `${ROOT_URL}/auth/login/`;
export const LOGOUT_URL = `${ROOT_URL}/auth/logout/`;
export const PASSWORD_CHANGE_URL = `${ROOT_URL}/auth/password/change/`;
export const REFRESH_TOKEN_URL = `${ROOT_URL}/auth/token/refresh/`;
export const USER_DATA_URL = `${ROOT_URL}/auth/user/`;
export const VERIFY_TOKEN_URL = `${ROOT_URL}/auth/token/verify/`;

export const LEAVES_URL = `${ROOT_URL}/leaves/`;
export const LEAVE_DETAIL_URL = (id: number | string) => `${LEAVES_URL}${id}/`;

export const NOTIFICATIONS_URL = `${ROOT_URL}/notifications/`;
export const NOTIFICATION_URL = (id: number | string) =>
  `${ROOT_URL}/notifications/${id}/`;

export const PROFILE_URL = `${ROOT_URL}/profile/`;

// Admin URLs
export const DEPARTMENTS_URL = `${ROOT_URL}/departments/`;
export const DEPARTMENT_URL = (id: number | string) => `${ROOT_URL}/departments/${id}/`;

export const EMPLOYEES_URL = `${ROOT_URL}/employees/`;
export const EMPLOYEE_URL = (id: number | string) => `${EMPLOYEES_URL}${id}/`;
export const EMPLOYEE_DEACTIVATE_URL = `${ROOT_URL}/employees/deactivate/`;
export const EMPLOYEE_PASSWORD_CHANGE_URL = `${ROOT_URL}/employees/password/change/`;
export const EMPLOYEE_EXPORT_URL = (_type: string) =>
  `${ROOT_URL}/employees/export/${_type}/`;

export const JOBS_URL = `${ROOT_URL}/jobs/`;
export const JOB_URL = (id: number | string) => `${ROOT_URL}/jobs/${id}/`;

export const LEAVES_ADMIN_URL = `${ROOT_URL}/leaves/admin/`;
export const LEAVE_ADMIN_DETAIL_URL = (id: number | string) =>
  `${ROOT_URL}/leaves/admin/${id}/`;
export const LEAVE_ADMIN_EXPORT_URL = (_type: string) =>
  `${ROOT_URL}/leaves/admin/export/${_type}/`;
