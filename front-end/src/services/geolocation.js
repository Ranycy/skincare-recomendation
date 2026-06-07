const GEOLOCATION_OPTIONS = {
  enableHighAccuracy: true,
  timeout: 10000,
  maximumAge: 300000,
};

function getGeolocationErrorMessage(error) {
  if (!navigator.geolocation) {
    return "Browser kamu tidak mendukung akses lokasi.";
  }

  if (error?.code === error.PERMISSION_DENIED) {
    return "Izin lokasi diperlukan untuk mengambil cuaca saat ini. Aktifkan izin lokasi lalu coba lagi.";
  }

  if (error?.code === error.TIMEOUT) {
    return "Pengambilan lokasi terlalu lama. Coba lagi sebentar lagi.";
  }

  return "Gagal mengambil lokasi saat ini. Coba lagi sebentar lagi.";
}

export function getCurrentLocation() {
  if (!navigator.geolocation) {
    return Promise.reject(new Error("Browser kamu tidak mendukung akses lokasi."));
  }

  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
          method: "gps",
        });
      },
      (error) => {
        reject(new Error(getGeolocationErrorMessage(error)));
      },
      GEOLOCATION_OPTIONS,
    );
  });
}

