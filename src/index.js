// Doorsturen van oude/alternatieve adressen naar https://hear.nl; verder statische site uit ./site.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname !== "hear.nl") {
      url.hostname = "hear.nl";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
